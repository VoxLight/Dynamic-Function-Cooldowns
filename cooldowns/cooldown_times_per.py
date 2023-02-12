from __future__ import annotations

import datetime

from asyncio import get_event_loop, AbstractEventLoop, Queue
from typing import TYPE_CHECKING, Optional

from cooldowns.exceptions import CallableOnCooldown, DynamicCallableOnCooldown

if TYPE_CHECKING:
    from cooldowns import Cooldown, DynamicCooldown

class CooldownTimesPer:
    def __init__(
        self,
        limit: int,
        time_period: float,
        _cooldown: Cooldown,
    ) -> None:
        """

        Parameters
        ----------
        limit: int
            How many items are allowed
        time_period: float
            The period of seconds limit applies to
        _cooldown: Cooldown
            A backref to the parent cooldown manager.

        Notes
        -----
        This is an internal object.
        You do not need to construct it yourself.
        """
        self.limit: int = limit
        self.time_period: float = time_period
        self._cooldown: Cooldown = _cooldown
        self.current: int = limit
        self.loop: AbstractEventLoop = get_event_loop()

        self._next_reset: Queue[datetime.datetime] = Queue()

    def __repr__(self):
        return f"<CooldownTimesPer(limit={self.limit}, current={self.current}, time_period={self.time_period})>"

    async def __aenter__(self) -> "CooldownTimesPer":
        if self.current == 0:
            raise CallableOnCooldown(
                self._cooldown.func, self._cooldown, self.next_reset
            )

        self.current -= 1

        self._next_reset.put_nowait(
            datetime.datetime.utcnow() + datetime.timedelta(seconds=self.time_period)
        )
        self.loop.call_later(self.time_period, self._reset_invoke)

        return self

    async def __aexit__(self, *_) -> None:
        ...

    @property
    def next_reset(self) -> Optional[datetime.datetime]:
        """When the next window is freed.

        Returns
        -------
        Optional[datetime.datetime]
            When the next window is freed.

            None if there are no windows.
        """
        try:
            # Needs to be a PEEK operand
            next_reset: datetime.datetime = self._next_reset._queue[0]  # type: ignore
        except IndexError:
            return None

        return next_reset

    @property
    def fully_reset_at(self) -> Optional[datetime.datetime]:
        """When this bucket is fully reset.

        Returns
        -------
        Optional[datetime.datetime]
            When this bucket fully resets.

        Notes
        -----
        This will return None if it
        is already fully reset.
        """
        try:
            # Try PEEK at the last entry if it exists
            next_reset: datetime.datetime = self._next_reset._queue[-1]  # type: ignore
        except IndexError:
            return None

        return next_reset

    def _reset_invoke(self):
        # Reset this cooldown by 'adding'
        # one more 'possible' call since
        # the current one is finished with it
        if self.current < 0:
            # Possible edge case?
            return None

        elif self.current == self.limit:
            # Don't ever give more windows
            # then the passed limit
            return None

        self.current += 1
        # Pop reset off queue
        self._next_reset.get_nowait()

    @property
    def has_cooldown(self) -> bool:
        """
        Is this instance currently tracking
        any cooldowns?

        If this returns False we can safely
        delete this instance from the
        :class:`Cooldown` lookup table.
        """
        return self.current != self.limit

class DynamicCooldownTimesPer(CooldownTimesPer):
    def __init__(
        self,
        limit: int,
        time_period: datetime.time,
        _cooldown: DynamicCooldown,
    ) -> None:
        """

        Parameters
        ----------
        limit: int
            How many items are allowed
        time_period: datetime.datetime
            The datetime when the cooldown expires
        _cooldown: Cooldown
            A backref to the parent cooldown manager.

        Notes
        -----
        This is an internal object.
        You do not need to construct it yourself.
        """
        self.limit: int = limit
        self.time_period: datetime.time = time_period
        self._cooldown: DynamicCooldown = _cooldown
        self.current: int = limit
        self.loop: AbstractEventLoop = get_event_loop()

        self._next_reset: Queue[datetime.datetime] = Queue()

    async def __aenter__(self) -> "DynamicCooldownTimesPer":
        if self.current == 0:
            raise DynamicCallableOnCooldown(
                self._cooldown.func, self._cooldown, self.next_reset
            )

        self.current -= 1

        reset = self.get_datetime_cooldown_resets()

        self._next_reset.put_nowait(reset)
        self.loop.call_later((reset - datetime.datetime.now()).total_seconds(), self._reset_invoke)

        return self

    def get_datetime_cooldown_resets(self) -> datetime.datetime:

        now = datetime.datetime.now().time()
        reset_time = datetime.datetime.combine(datetime.date.today(), self.time_period)

        if reset_time.time() < now:
            reset_time = reset_time.replace(day=reset_time.day + 1)

        return reset_time


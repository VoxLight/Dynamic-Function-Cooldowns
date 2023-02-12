from collections import namedtuple

from .buckets import CooldownBucket, SlashBucket
from .protocols import CooldownBucketProtocol
from .cooldown import Cooldown, DynamicCooldown, cooldown, shared_cooldown, dynamic_cooldown
from .cooldown_times_per import CooldownTimesPer, DynamicCooldownTimesPer
from .exceptions import (
    CallableOnCooldown,
    DynamicCallableOnCooldown,
    NoRegisteredCooldowns,
    UnknownBucket,
    CooldownAlreadyExists,
)
from .utils import (
    get_remaining_calls,
    reset_cooldown,
    reset_cooldowns,
    reset_bucket,
    get_cooldown,
    define_shared_cooldown,
    get_shared_cooldown,
)

__all__ = (
    "CooldownBucket",
    "SlashBucket",
    "Cooldown",
    "DynamicCooldown"
    "cooldown",
    "shared_cooldown",
    "CooldownTimesPer",
    "DynamicCooldownTimesPer",
    "CooldownBucketProtocol",
    "CallableOnCooldown",
    "DynamicCallableOnCooldown",
    "NoRegisteredCooldowns",
    "CooldownAlreadyExists",
    "get_remaining_calls",
    "UnknownBucket",
    "reset_cooldowns",
    "reset_bucket",
    "reset_cooldown",
    "get_cooldown",
    "define_shared_cooldown",
    "get_shared_cooldown",
)

__version__ = "1.7.0"
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=7, micro=0, releaselevel="final", serial=0)

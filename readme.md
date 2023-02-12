Function Cooldowns
---

A simplistic take on functional cooldowns. 

`pip install function-cooldowns`


---

### Example usage

A simplistic example, read more on the docs!

```python
import cooldowns

...

@bot.slash_command(
    description="Ping command",
)
@cooldowns.cooldown(1, 15, bucket=cooldowns.SlashBucket.author)
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message("Pong!")
```
### Dynamic Cooldowns

Have a function reset at a certain time every day.

```python
import datetime
...

five_am = datetime.time(hour=5, minute=0, second=0)

@bot.slash_command(
    description="Daily Coins",
)
@cooldowns.dynamic_cooldown(1, five_am, bucket=cooldowns.SlashBucket.author)
async def coins(interaction: nextcord.Interaction):
    await interaction.response.send_message("You have claimed your daily coins!")
```


---

#### Find more examples [here](https://function-cooldowns.readthedocs.io/en/latest/modules/examples.html).

#### For documentation, please see [here](https://function-cooldowns.readthedocs.io/en/latest/).

#### This implements the [leaky bucket](https://en.wikipedia.org/wiki/Leaky_bucket) algorithm

---

### Support

Want realtime help? Join the discord [here](https://discord.gg/BqPNSH2jPg).

---

### Funding

Want a feature added quickly? Want me to help build your software using this?

Sponsor me [here](https://github.com/sponsors/Skelmis)

# dpy-components
[![PyPI](https://img.shields.io/pypi/v/discord-emoji)](https://pypi.org/project/discord-emoji) 
[![PyPI - Downloads](https://img.shields.io/badge/dynamic/json?label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fdiscord-emoji)](https://pepy.tech/project/discord-emoji/) 
[![Documentation Status](https://readthedocs.org/projects/dpy-components/badge/?version=latest)](https://dpy-components-ja.readthedocs.io/en/latest/?badge=latest)  
This lib adds components support for discord.py.  
Please note this is beta yet.

Example
=====

```python
import os

from discord.ext import commands, components

bot = commands.Bot("c ")
bot.load_extension("discord.ext.components")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def test(ctx, button_label, hidden: bool):
    await components.send(ctx, "Click this", components=[components.Button(button_label, name="button1")])
    cmp = await bot.wait_for("button_click", check=lambda c: c.name == "button1")
    await cmp.send(f"You clicked {button_label}.", hidden=hidden)

bot.run(os.getenv("token"))

```

Reference
=========
### `ButtonType`
Represents button type.
#### `primary`,`primary_cta`,`blue`,`blurple`
Represents `1`.
#### `success`,`primary_success`,`green`
Represents `2`.
#### `secondary`,`gray`,`grey`
Represents `3`.
### `danger`,`destructive`,`red`
Represents `4`.
### `link`,`url`
Represents `5`.
#### `components.send`
This function is a coroutine.
Send message with components.
```python
components.send(channel: discord.abc.Messageable, content=None, *, tts=False, embed=None, file=None,
                files=None, delete_after=None, nonce=None,
                allowed_mentions=None, reference=None,
                mention_author=None, components=[])
```
`channnel`: Channel to send the message.  
`content`..`mention_author`: Same as `discord.abc.Messageable.send`.  
`components`: Components to attach to the message.  
If you want to use multi row components, please specify 2D list.  
#### `components.reply`
This function is a coroutine.  
An utility function for replying message.  
Same as:
```py
await send(target.channel, *args, reference=target.to_reference(), **kwargs)
```
#### `components.Button`
Represents a button in component.  
`label`: Label for the button.  
`custom_id`|`name`: Custom id for the button.  
`url`: URL for the button.  
`style`: Style for the button.  
Pass values of [Button Styles](https://discord.com/developers/docs/interactions/message-components#buttons-button-styles), or `ButtonType`.  
`emoji`: Emoji for the button.  
`enabled`: Whether the button is enabled.  
##### Properties
`.disabled`: Same as `not self.enabled`.  
### `on_button_click(cmp: ButtonResponse)`
Fires when user clicked button.  
## ButtonResponse
Represents a button response.  
Do not initialize this class directly.  
`id`: ID of the interaction.  
`application_id`: Application ID of the interaction.  
`guild`: Guild of the interaction.  
`channel`: Channel of the interaction.  
`message`: Message of the interaction.  
`member`: Member who pressed the button.  
`token`: Token of the interaction.  
`custom_id`|`name`: Custom ID of the button.  

#### `ButtonResponse.send`
This function is a coroutine.  
Responds interaction.  
```python
ButtonResponse.send(
    content=None, *,
    embed=None,
    embeds=[],
    allowed_mentions=None,
    tts=False,
    hidden=False
)
```
`content`...`tts`: Same as `discord.abc.Messageable.send`.  
`hidden`: Hide the message or not.  
#### `ButtonResponse.defer_source`
This function is a coroutine.  
ACK an interaction with DeferredChannelMessageWithSource(5).  
The user sees a loading state.  
#### `ButtonResponse.defer_update`
This function is a coroutine.  
ACK an interaction with DeferredUpdateMessage(6).  
The user doesn't see a loading state.  

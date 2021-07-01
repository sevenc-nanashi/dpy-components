from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, List

import discord
from discord import File, AllowedMentions
from discord import utils
from discord.emoji import Emoji
from discord.errors import InvalidArgument
from discord.ext import commands
from discord.http import Route


def _convert_style(style):
    if isinstance(style, int):
        if not 1 <= style <= 5:
            raise TypeError("style should be in 1 to 5.")
        return style
    elif isinstance(style, ButtonType):
        return style.value
    else:
        raise TypeError("style should be int or ButtonType.")


def _convert_components(components):
    listed_components = []
    temp_components = []
    for component in components:
        if isinstance(component, list):
            if temp_components:
                listed_components.append(temp_components)
                temp_components = []
            listed_components.append(component)
        elif isinstance(component, SelectMenu):
            if temp_components:
                listed_components.append(temp_components)
                temp_components = []
            listed_components.append([component])
        else:
            temp_components.append(component)
    if temp_components:
        listed_components.append(temp_components)
    listed_components = list(map(lambda c: {"type": 1, "components": list(map(lambda co: co.to_dict(), c))}, listed_components))

    return listed_components


class ButtonType(Enum):
    """Represents button type."""
    primary = 1
    primary_cta = 1
    secondary = 2
    success = 3
    primary_success = 3
    danger = 4
    destructive = 4
    link = 5
    url = 5

    blue = 1
    blurple = 1
    gray = 2
    grey = 2
    green = 3
    red = 4


@dataclass
class Button:
    """Represents a button in component.

    Parameters
    ----------
    label : str
        Label for the button.
    custom_id : Optional[str]
        Custom id for the button.
    style : Union[int, ButtonType]
        Style for the button.
    url : Optional[str]
        URL for the button.
    emoji : Union[Emoji, str]
        Emoji for the button.
    enabled : bool
        Weather button is enabled or disabled.
    """
    label: str
    custom_id: Optional[str] = None
    style: Union[int, ButtonType] = ButtonType.blurple
    url: Optional[str] = None
    emoji: Union[Emoji, str] = None
    enabled: bool = True
    name: str = None

    def to_dict(self):
        res = {
            "type": 2,
            "style": _convert_style(self.style),
            "label": self.label,
            "disabled": not self.enabled
        }
        if self.emoji:
            if isinstance(self.emoji, str):
                res["emoji"] = {"name": self.emoji}
            else:
                res["emoji"] = {
                    "id": self.emoji.id,
                    "name": self.emoji.name,
                    "animated": self.emoji.animated
                }
        if self.name or self.custom_id:
            res["custom_id"] = self.custom_id or self.name
        if self.url:
            res["url"] = self.url
        return res


@dataclass
class SelectOption:
    """Represents a option for the select menu.

    Parameters
    ----------
    label : str
        Label for the option.
    value : str
        Value for the option.
    description : Optional[str]
        Description for the option.
    emoji : Union[Emoji, str]
        Emoji for the option.
    default : bool
        Weather option is default.
    """
    label: str
    value: str
    description: Optional[str] = None
    emoji: Union[Emoji, str] = None
    default: bool = False

    def to_dict(self):
        res = {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "default": self.default
        }
        if self.emoji:
            if isinstance(self.emoji, str):
                res["emoji"] = {
                    "name": self.emoji,
                    "id": None
                }
            else:
                res["emoji"] = {
                    "name": self.emoji.name,
                    "id": self.emoji.id,
                }

        return res


@dataclass
class SelectMenu:
    """Represents a select menu in component.

    Parameters
    ----------
    custom_id : Optional[str]
        Custom id for the select menu.
    options : List[SelectOption]
        Options for the select menu.
    placeholder : Optional[str]
        Placeholder for the select menu.
    min_values : int
        Minimum number of items that must be chosen.
    max_values: int
        Maximum number of items that must be chosen.
    """
    custom_id: Optional[str]
    options: List[SelectOption]
    placeholder: Optional[str] = None
    min_values: int = 1
    max_values: int = 1

    def to_dict(self):
        res = {
            "type": 3,
            "custom_id": self.custom_id,
            "options": [o.to_dict() for o in self.options],
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values
        }
        return res


async def _send_files(self, channel_id, *, files, content=None, tts=False, embeds=None, nonce=None, allowed_mentions=None, message_reference=None, components=None):
    r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)
    form = []

    payload = {'tts': tts}
    if content:
        payload['content'] = content
    if embeds:
        payload['embed'] = embeds
    if nonce:
        payload['nonce'] = nonce
    if allowed_mentions:
        payload['allowed_mentions'] = allowed_mentions
    if message_reference:
        payload['message_reference'] = message_reference
    if components:
        payload['components'] = components
    form.append({'name': 'payload_json', 'value': utils.to_json(payload)})
    if len(files) == 1:
        file = files[0]
        form.append({
            'name': 'file',
            'value': file.fp,
            'filename': file.filename,
            'content_type': 'application/octet-stream'
        })
    else:
        for index, file in enumerate(files):
            form.append({
                'name': 'file%s' % index,
                'value': file.fp,
                'filename': file.filename,
                'content_type': 'application/octet-stream'
            })

    return self.request(r, form=form, files=files)


async def send(channel, content=None, *, tts=False, embed=None, embeds=None, file=None,
               files=None, delete_after=None, nonce=None,
               allowed_mentions=None, reference=None,
               mention_author=None, components=[]):
    """Send message with components.

    Parameters
    ----------
    channel : discord.abc.Messageable
        Channel to send the message.
    content..mention_author
        Same as ``discord.abc.Messageable.send``.
    components : list, optional
        Components to attach to the message.
        Specify 2D list if you want to use multi row components.

    Returns
    -------
    Message
        Message was sent.
    """
    channel = await channel._get_channel()
    state = channel._state
    components2 = []
    if not components:
        pass
    else:
        components2 = _convert_components(components)
    content = str(content) if content is not None else None
    if embed is not None and embeds is not None:
        raise InvalidArgument('cannot pass both embed and embeds parameter to send()')
    if embed is not None:
        embeds = [embed]
    if embeds is not None:
        embeds = list(map(lambda e: e.to_dict(), embeds))

    if allowed_mentions is not None:
        if state.allowed_mentions is not None:
            allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
        else:
            allowed_mentions = allowed_mentions.to_dict()
    else:
        allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()

    if mention_author is not None:
        allowed_mentions = allowed_mentions or AllowedMentions().to_dict()
        allowed_mentions['replied_user'] = bool(mention_author)

    if reference is not None:
        try:
            reference = reference.to_message_reference_dict()
        except AttributeError:
            raise InvalidArgument('reference parameter must be Message or MessageReference') from None

    if file is not None and files is not None:
        raise InvalidArgument('cannot pass both file and files parameter to send()')

    if file is not None:
        if not isinstance(file, File):
            raise InvalidArgument('file parameter must be File')

        try:
            data = await _send_files(channel.id, files=[file], allowed_mentions=allowed_mentions,
                                     content=content, tts=tts, embeds=embeds, nonce=nonce,
                                     message_reference=reference, components=components2)
        finally:
            file.close()

    elif files is not None:
        if len(files) > 10:
            raise InvalidArgument('files parameter must be a list of up to 10 elements')
        elif not all(isinstance(file, File) for file in files):
            raise InvalidArgument('files parameter must be a list of File')

        try:
            data = await _send_files(channel.id, files=files, content=content, tts=tts,
                                     embeds=embeds, nonce=nonce, allowed_mentions=allowed_mentions,
                                     message_reference=reference, components=components2)
        finally:
            for f in files:
                f.close()
    else:
        r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel.id)
        payload = {}

        if content:
            payload['content'] = content

        if tts:
            payload['tts'] = True

        if embeds:
            payload['embeds'] = embeds

        if nonce:
            payload['nonce'] = nonce

        if allowed_mentions:
            payload['allowed_mentions'] = allowed_mentions

        if reference:
            payload['message_reference'] = reference

        if components2:
            payload['components'] = components2

        data = await state.http.request(r, json=payload)

    ret = state.create_message(channel=channel, data=data)

    if delete_after is not None:
        await ret.delete(delay=delete_after)
    return ret


async def edit(message, **fields):
    try:
        content = fields['content']
    except KeyError:
        pass
    else:
        if content is not None:
            fields['content'] = str(content)

    try:
        embed = fields['embed']
    except KeyError:
        pass
    else:
        if embed is not None:
            fields['embed'] = embed.to_dict()

    try:
        suppress = fields.pop('suppress')
    except KeyError:
        pass
    else:
        flags = discord.MessageFlags._from_value(message.flags.value)
        flags.suppress_embeds = suppress
        fields['flags'] = flags.value

    delete_after = fields.pop('delete_after', None)

    try:
        allowed_mentions = fields.pop('allowed_mentions')
    except KeyError:
        if message._state.allowed_mentions is not None and message.author.id == message._state.self_id:
            fields['allowed_mentions'] = message._state.allowed_mentions.to_dict()
    else:
        if allowed_mentions is not None:
            if message._state.allowed_mentions is not None:
                allowed_mentions = message._state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
            fields['allowed_mentions'] = allowed_mentions

    try:
        attachments = fields.pop('attachments')
    except KeyError:
        pass
    else:
        fields['attachments'] = [a.to_dict() for a in attachments]

    components2 = []
    components = fields.get("components")
    if components:
        if isinstance(components[0], list):
            components2 = [{
                "type": 1,
                "components": list(map(lambda b: b.to_dict(), c)),
            }
                for c in components]
        else:
            components2 = [{
                "type": 1,
                "components": list(map(lambda b: b.to_dict(), components)),
            }]
        fields["components"] = components2

    if fields:
        data = await message._state.http.edit_message(message.channel.id, message.id, **fields)
        message._update(data)

    if delete_after is not None:
        await message.delete(delay=delete_after)


async def reply(target, *args, **kwargs):
    """An utility function for replying message."""
    if isinstance(target, commands.Context):
        reference = target.message.to_reference()
    else:
        reference = target.to_reference()
    return await send(target.channel, *args, reference=reference, **kwargs)

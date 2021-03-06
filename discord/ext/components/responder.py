import discord
from discord.http import Route
from .sender import _convert_components


class ButtonResponse():
    """
    Represents a button response.
    Do not initialize this class directly.
    """

    def __init__(self, bot, data, state):
        self.bot = bot
        self.state = state
        self.data = data

    async def _fetch(self):
        bot = self.bot
        data = self.data
        self.id = int(data["id"])
        self.application_id = int(data["application_id"])
        if data.get("guild_id") is None:
            self.guild = None
            self.user = discord.User(state=bot._get_state(), data=data["user"])
            self.member = None
        else:
            self.guild = bot.get_guild(int(data["guild_id"]))
            self.member = discord.Member(state=bot._get_state(), guild=self.guild, data=data["member"])
            self.user = None
        self.channel = bot.get_channel(int(data["channel_id"]))
        if data["message"].get("message_reference") and data["message"]["message_reference"].get("channel_id") is None:
            data["message"]["message_reference"]["channel_id"] = data["channel_id"]

        if data["message"]["flags"] == 64:
            try:
                self.message = await self.channel.fetch_message(int(data["message"]["id"]))
            except discord.errors.NotFound:
                self.message = discord.PartialMessage(channel=self.channel, id=int(data["message"]["id"]))
        else:
            self.message = discord.Message(state=bot._get_state(), channel=self.channel, data=data["message"])
        self.token = data["token"]
        self.custom_id = data["data"]["custom_id"]
        self.name = data["data"]["custom_id"]
        self.defered = False
        self.sent_callback = False

    @property
    def fired_by(self):
        """Return ``self.member`` or ``self.user``."""
        return self.member or self.user

    async def defer_source(self, hidden=False):
        """
        ACK an interaction with DeferredChannelMessageWithSource(5).
        The user sees a loading state.

        Parameters
        ----------
        hidden : bool
            Hide interaction response or not.
        """
        if self.defered:
            raise "Already defered."
        r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=self.id, interaction_token=self.token)
        self.defered = True
        await self.bot.http.request(r, json={"type": 5, "data": {"flags": 64 if hidden else 0}})

    async def defer_update(self):
        """
        ACK an interaction with DeferredUpdateMessage(6).
        The user doesn't see a loading state.

        Parameters
        ----------
        hidden : bool
            Hide interaction response or not.
        """
        if self.defered:
            raise "Already defered."
        r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=self.id, interaction_token=self.token)
        self.defered = True
        await self.bot.http.request(r, json={"type": 6})

    async def send(self, content=None, *, embed=None, embeds=[], allowed_mentions=None, hidden=False, tts=False, components=[]):
        """Responds interaction.

        Parameters
        ----------
        content...tts
            Same as ``discord.abc.Messageable.send``.
        hidden : bool
            Hide the message or not.
        """
        state = self.state
        content = str(content) if content is not None else None
        components2 = []
        if not components:
            pass
        else:
            components2 = _convert_components(components)
        if embed is not None:
            if embeds:
                raise ValueError("You mustn't specify embed and embeds same time.")
            else:
                embeds = [embed]

        if allowed_mentions is not None:
            if state.allowed_mentions is not None:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()
        if self.sent_callback:
            r = Route('POST', "/webhooks/{application_id}/{interaction_token}", application_id=self.application_id, interaction_token=self.token)
            data = await state.http.request(r, json={
                "content": content,
                "tts": tts,
                "embeds": list(map(lambda e: e.to_dict(), embeds)),
                "allowed_mentions": allowed_mentions,
                "flags": 64 if hidden else 0,
                "components": components2
            })
        elif self.defered:
            r = Route('PATCH', "/webhooks/{application_id}/{interaction_token}/messages/@original", application_id=self.application_id, interaction_token=self.token)
            data = await state.http.request(r, json={
                "content": content,
                "tts": tts,
                "embeds": list(map(lambda e: e.to_dict(), embeds)),
                "allowed_mentions": allowed_mentions,
                "flags": 64 if hidden else 0,
                "components": components2
            })
            self.sent_callback = True
        else:
            r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=self.id, interaction_token=self.token)
            data = await state.http.request(r, json={
                "type": 4,
                "data": {
                    "content": content,
                    "tts": tts,
                    "embeds": list(map(lambda e: e.to_dict(), embeds)),
                    "allowed_mentions": allowed_mentions,
                    "flags": 64 if hidden else 0,
                    "components": components2
                }
            })
            self.sent_callback = True
        self.defered = True
        if data:
            ret = state.create_message(channel=self.channel, data=data)
            return ret

    async def _get_channel(self):
        return self.channel


class SelectMenuResponse():
    """
    Represents a select menu response.
    Do not initialize this class directly.
    """

    def __init__(self, bot, data, state):
        self.bot = bot
        self.state = state
        self.data = data

    async def _fetch(self):
        bot = self.bot
        data = self.data
        self.id = int(data["id"])
        self.application_id = int(data["application_id"])
        if data.get("guild_id") is None:
            self.guild = None
            self.user = discord.User(state=bot._get_state(), data=data["user"])
            self.member = None
        else:
            self.guild = bot.get_guild(int(data["guild_id"]))
            self.member = discord.Member(state=bot._get_state(), guild=self.guild, data=data["member"])
            self.user = None
        self.channel = bot.get_channel(int(data["channel_id"]))
        if data["message"].get("message_reference") and data["message"]["message_reference"].get("channel_id") is None:
            data["message"]["message_reference"]["channel_id"] = data["channel_id"]
        if data["message"]["flags"] == 64:
            try:
                self.message = await self.channel.fetch_message(int(data["message"]["id"]))
            except discord.errors.NotFound:
                self.message = discord.PartialMessage(channel=self.channel, id=int(data["message"]["id"]))
        else:
            self.message = discord.Message(state=bot._get_state(), channel=self.channel, data=data["message"])
        self.token = data["token"]
        self.custom_id = data["data"]["custom_id"]
        self.name = data["data"]["custom_id"]
        self.values = data["data"].get("values", [])
        self.defered = False
        self.sent_callback = False

    @property
    def value(self):
        """Return the first value of ``values`` or ``None``."""
        if self.values:
            return self.values[0]
        else:
            return None

    @property
    def fired_by(self):
        """Return ``self.member`` or ``self.user``."""
        return self.member or self.user

    async def defer_source(self, hidden=False):
        """
        ACK an interaction with DeferredChannelMessageWithSource(5).
        The user sees a loading state.

        Parameters
        ----------
        hidden : bool
            Hide interaction response or not.
        """
        if self.defered:
            raise "Already defered."
        r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=self.id, interaction_token=self.token)
        self.defered = True
        await self.bot.http.request(r, json={"type": 5, "data": {"flags": 64 if hidden else 0}})

    async def defer_update(self):
        """
        ACK an interaction with DeferredUpdateMessage(6).
        The user doesn't see a loading state.

        Parameters
        ----------
        hidden : bool
            Hide interaction response or not.
        """
        if self.defered:
            raise "Already defered."
        r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=self.id, interaction_token=self.token)
        self.defered = True
        await self.bot.http.request(r, json={"type": 6})

    async def send(self, content=None, *, embed=None, embeds=[], allowed_mentions=None, hidden=False, tts=False):
        """Responds interaction.

        Parameters
        ----------
        content...tts
            Same as ``discord.abc.Messageable.send``.
        hidden : bool
            Hide the message or not.
        """
        state = self.state
        content = str(content) if content is not None else None
        if embed is not None:
            if embeds:
                raise ValueError("You mustn't specify embed and embeds same time.")
            else:
                embeds = [embed]

        if allowed_mentions is not None:
            if state.allowed_mentions is not None:
                allowed_mentions = state.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            allowed_mentions = state.allowed_mentions and state.allowed_mentions.to_dict()
        if self.sent_callback:
            r = Route('POST', "/webhooks/{application_id}/{interaction_token}", application_id=self.application_id, interaction_token=self.token)
            data = await state.http.request(r, json={
                "content": content,
                "tts": tts,
                "embeds": list(map(lambda e: e.to_dict(), embeds)),
                "allowed_mentions": allowed_mentions,
                "flags": 64 if hidden else 0
            })
        elif self.defered:
            r = Route('PATCH', "/webhooks/{application_id}/{interaction_token}/messages/@original", application_id=self.application_id, interaction_token=self.token)
            data = await state.http.request(r, json={
                "content": content,
                "tts": tts,
                "embeds": list(map(lambda e: e.to_dict(), embeds)),
                "allowed_mentions": allowed_mentions,
                "flags": 64 if hidden else 0
            })
            self.sent_callback = True
        else:
            r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=self.id, interaction_token=self.token)
            data = await state.http.request(r, json={
                "type": 4,
                "data": {
                    "content": content,
                    "tts": tts,
                    "embeds": list(map(lambda e: e.to_dict(), embeds)),
                    "allowed_mentions": allowed_mentions,
                    "flags": 64 if hidden else 0
                }
            })
            self.sent_callback = True
        self.defered = True
        ret = state.create_message(channel=self.channel, data=data)
        return ret

    async def _get_channel(self):
        return self.channel

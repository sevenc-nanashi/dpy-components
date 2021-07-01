from discord.ext import commands
from .responder import ButtonResponse, SelectMenuResponse


class ComponentCog(commands.Cog):
    def __init__(self, bot):
        global Guild_settings, Texts
        global get_txt
        self.bot = bot

    @commands.Cog.listener()
    async def on_socket_response(self, pl):
        if pl["t"] != "INTERACTION_CREATE":
            return
        data = pl["d"]
        if data["type"] != 3:
            return
        if data["data"]["component_type"] == 2:
            resp = ButtonResponse(self.bot, data, self.bot._get_state())
            await resp._fetch()
            self.bot.dispatch("button_click", resp)
        elif data["data"]["component_type"] == 3:
            resp = SelectMenuResponse(self.bot, data, self.bot._get_state())
            await resp._fetch()
            self.bot.dispatch("menu_select", resp)


def setup(_bot):
    global bot
    bot = _bot
    _bot.add_cog(ComponentCog(_bot))

from .sender import send, edit, reply, Button, ButtonType, SelectMenu, SelectOption  # noqa
from .receiver import ComponentCog  # noqa
from .responder import ButtonResponse, SelectMenuResponse  # noqa

__version__ = "0.3.2"


def setup(bot):
    bot.add_cog(ComponentCog(bot))

from .sender import send, edit, reply, Button, ButtonType  # noqa
from .receiver import ComponentCog  # noqa
from .responder import ButtonResponse  # noqa

__version__ = "0.2.4"


def setup(bot):
    bot.add_cog(ComponentCog(bot))

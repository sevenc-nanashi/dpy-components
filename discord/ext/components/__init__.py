from .sender import send, edit, Button  # noqa
from .receiver import ComponentCog  # noqa
from .responder import ButtonResponse  # noqa

__version__ = "0.0.2"


def setup(bot):
    bot.add_cog(ComponentCog(bot))

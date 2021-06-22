API documentation
==================

Receive components' event
-------------------------
.. class:: components.ComponentsCog
   
   A cog that receive and handles components' event.
   You can load this cog as extension with:  

   .. code-block:: python

      bot.load_extension("discord.ext.components")

events
~~~~~~

.. function:: on_button_click(com)

   Fires when user clicked button.
   
   :param com: A response.
   :type com: :class:`components.ButtonResponse`

Respond components' event
------------------------
.. autoclass:: components.ButtonResponse
   :members:

Send messages with components
---------------
.. autofunction:: components.send

.. autofunction:: components.reply
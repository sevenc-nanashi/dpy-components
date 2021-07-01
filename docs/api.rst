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

.. function:: on_menu_select(com)

   Fires when user selected menu.
   
   :param com: A response.
   :type com: :class:`components.SelectMenuResponse`

Respond components' event
-------------------------
.. autoclass:: components.ButtonResponse
   :members:

.. autoclass:: components.SelectMenuResponse
   :members:

Send messages with components
-----------------------------
.. autofunction:: components.send

.. autofunction:: components.reply

Components
~~~~~~~~~~
.. autoclass:: components.Button
   :members:

.. autoclass:: components.SelectMenu
   :members:

.. autoclass:: components.SelectOption
   :members:
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

Styles
~~~~~~

.. class:: components.ButtonType

   Represents style of button.
   
   .. attribute:: primary
   .. attribute:: primary_cta
   .. attribute:: blue
   .. attribute:: blurple
      
      Represents style ``1``.

   .. attribute:: secondary
   .. attribute:: gray
   .. attribute:: grey

      Represents style ``2``.
   
   .. attribute:: success
   .. attribute:: primary_success
   .. attribute:: green

      Represents style ``3``.

   .. attribute:: danger
   .. attribute:: destructive
   .. attribute:: red

      Represents style ``4``.

   .. attribute:: link
   .. attribute:: url
      
      Represents style ``5``.

   
      
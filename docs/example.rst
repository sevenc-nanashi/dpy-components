Examples
========

Send button and receive
-----------------------

.. code-block:: python

    import os

    from discord.ext import commands, components

    bot = commands.Bot("c ")
    bot.load_extension("discord.ext.components")


    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))


    @bot.command()
    async def test(ctx, button_label, hidden: bool):
        await components.send(ctx, "Click this", components=[components.Button(button_label, custom_id="button1")])
        com = await bot.wait_for("button_click", check=lambda c: c.name == "button1")
        await com.send(f"You clicked {button_label}.", hidden=hidden)

    bot.run(os.getenv("token"))

Authorization button
--------------------

.. code-block:: python
    
    import os

    import discord
    from discord.ext import commands, components

    bot = commands.Bot("c ")
    bot.load_extension("discord.ext.components")


    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))


    @bot.command()
    async def send_auth(ctx):
        await components.send(ctx, "Click this button to get your member role", components=[components.Button("Get member role", custom_id="get_auth_role", style=components.ButtonType.green)])


    @bot.event
    async def on_button_click(com):
        if com.custom_id == "get_auth_role":
            await com.defer_source(hidden=True)
            role = discord.utils.get(com.guild.roles, name="Member")
            if role in com.member.roles:
                await com.send("You already have your member role.")
            else:
                await com.member.add_roles(role)
                await com.send("You got your member role. Enjoy!")

    bot.run(os.getenv("token"))

Pagenation with select menu
---------------------------

.. code-block:: python

    import asyncio
    import os

    import discord
    from discord.ext import commands
    from discord.ext import components
    bot = commands.Bot("c ")
    bot.load_extension("discord.ext.components")

    pages = [
        "Done is better than perfect.\n\n--Mark Zuckerberg",
        "The best way to predict the future is to invent it.\n\n--Alan Key",
        "Programs must be written for people to read, and only incidentally for machines to execute.\n\n--Hal Alverson"
    ]


    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))


    @bot.command()
    async def send_page(ctx):
        options = []
        for i, _ in enumerate(pages, 1):
            options.append(components.SelectOption(f"Page {i}", f"pagenation_{i}"))
        msg = await components.send(ctx, "Use select menu for switch page", components=[
            components.SelectMenu("pagenation", options, "Select page...")
        ])
        try:
            while True:
                com = await bot.wait_for("menu_select", check=lambda c: c.message == msg, timeout=30)
                page = int(com.value.removeprefix("pagenation_"))
                await com.send(pages[page - 1] + f"\n\n`Page {page}`", hidden=True)
        except asyncio.TimeoutError:
            return


    bot.run(os.getenv("discord_bot_token"))


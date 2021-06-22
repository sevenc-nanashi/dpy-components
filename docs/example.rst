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

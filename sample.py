import os

from discord.ext import commands, components

bot = commands.Bot("c ")
bot.load_extension("discord.ext.components")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def test(ctx, button_label, hidden: bool):
    await components.send(ctx, "Click this", components=[components.Button(button_label, name="button1")])
    cmp = await bot.wait_for("button_click", check=lambda c: c.name == "button1")
    await cmp.send(f"You clicked {button_label}.", hidden=hidden)

bot.run(os.getenv("token"))

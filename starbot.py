from discord.ext import commands
import subprocess, asyncio, json
from time import sleep

from lib.botController import botControllerClass

bot = commands.Bot(command_prefix = "")
bot.remove_command('help')

sleep(0.1)

try:
    bot.config = json.loads(open("data/config.json", "r").read())
except:
    open("data/config.json", "w").write('{"minecraft":{"email":"","password":"","serverAddress":"creative.starlegacy.net","connectionCooldown":500},"discord":{"token":"","botMaster":0,"botControllers":[0]}}')

bot.botController = botControllerClass()

bot.command_prefix = ">"

@commands.command()
async def help(ctx):
    await ctx.send("""**StarBot v1.0.5**

Commands:
>playerInfo (>playerinfo / >pi) : Gets details about a player
>nationInfo (>nationinfo / >ni) : Gets details about a nation
>settlementInfo (>settlementinfo / >si) : Gets details about a settlement
>botControl (>botcontrol / >bc) : Restricted Command
>botControl shutdown : Restricted Command - Shuts down the bot
>botControl disable : Restricted Command - Prevents the bot from connecting to minecraft
>botControl enable : Restricted Command - Allows the bot to connect to minecraft

Bot Discord Server: https://discord.gg/cPkrrrj""")

@bot.command(aliases = ["botcontrol", "bc"])
async def botControl(ctx, subcommand = ""):
    if subcommand == "shutdown":
        if not ctx.message.author.id == bot.config["discord"]["botMaster"]:
            await ctx.send("Access Denied.")
            return

        await ctx.send("Shutting Down")
        await ctx.bot.logout()
        
    elif subcommand == "disable":
        if not ctx.message.author.id in bot.config["discord"]["botControllers"] and not ctx.message.author.id == bot.config["discord"]["botMaster"]:
            await ctx.send("Access Denied. Please contact PeterCrawley if this should not be the case.")
            return

        bot.botController.disabled = True

        await ctx.send("Disabled")

    elif subcommand == "enable":
        if not ctx.message.author.id in bot.config["discord"]["botControllers"] and not ctx.message.author.id == bot.config["discord"]["botMaster"]:
            await ctx.send("Access Denied. Please contact PeterCrawley if this should not be the case.")
            return

        bot.botController.disabled = False

        await ctx.send("Enabled")

    else:
        await ctx.send("Invalid subcommand.")

@bot.event
async def on_ready():
    bot.remove_command("help")
    bot.add_command(help)

loop = asyncio.get_event_loop()

loop.create_task(bot.botController.activeCheck())

bot.load_extension("cogs.utils")

bot.run(bot.config["discord"]["token"])
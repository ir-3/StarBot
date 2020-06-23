from discord.ext import commands
import subprocess, asyncio, json
from time import sleep

from lib.botController import botControllerClass
import lib.verificationHandler as verificationHandler

bot = commands.Bot(command_prefix = "")
bot.remove_command('help')

sleep(0.1)

bot.config = json.loads(open("data/config.json", "r").read())

bot.botController = botControllerClass()

bot.command_prefix = bot.config["discord"]["prefix"]

@commands.command()
async def help(ctx):
	await ctx.send("""**StarBot v1.1.4**

Commands:
>playerInfo (>playerinfo / >pi) : Gets details about a player
>nationInfo (>nationinfo / >ni) : Gets details about a nation
>nationTop (>nt / >ntop / >nationtop) : Nation Leaderboard
>settlementInfo (>settlementinfo / >si) : Gets details about a settlement
>settlementTop (>st / >stop / >settlementtop) : Settlement Leaderboard

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
loop.create_task(verificationHandler.handleExpiredCodes())

bot.load_extension("cogs.utils")
bot.load_extension("cogs.verification")

bot.run(bot.config["discord"]["token"])
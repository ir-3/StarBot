import logging, sys, datetime, json, asyncio
from lib.botController import botControllerClass
from discord.ext import commands

# Inilize Logging
logging.basicConfig(filename = f"{datetime.datetime.now().strftime('%x %X').replace('/', '-')}.log", level = logging.INFO, format = "%(levelname)s / %(filename)s(%(lineno)d) / %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)s / %(filename)s(%(lineno)d) / %(message)s"))

logging.getLogger().addHandler(console)

logging.info("Starting Starbot")

# Load discord.py
logging.info("Loading discord.py")

bot = commands.Bot(command_prefix = "")
bot.remove_command('help') # We want to use our own help command.

# Load config
logging.info("Loading config")

bot.config = json.loads(open("data/config.json", "r").read())
bot.command_prefix = bot.config["discord"]["prefix"]

# Load BotController
# TODO: Bot Controller is a legacy class left over from 1.X.X
logging.info("Loading botController")

bot.botController = botControllerClass() 

# Load Cogs
logging.info("Loading cogs")

loop = asyncio.get_event_loop()

loop.create_task(bot.botController.activeCheck())
bot.load_extension("cogs.utils")

bot.load_extension("cogs.misc")
bot.load_extension("cogs.botControl")

# Events
@bot.event
async def on_ready():
	logging.info("Bot has started")

@bot.event
async def on_command(context):
	logging.info(f"{context.message.author.name}#{context.message.author.discriminator} ran the command {context.command} with perameters {str(context.args[2:])}.")

# Start
logging.info("Starting")

bot.run(bot.config["discord"]["token"])
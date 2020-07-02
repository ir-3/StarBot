from discord.ext import commands

class botControl(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ["botcontrol", "bc"])
	async def botControl(self, ctx, subcommand = ""):
		if subcommand == "shutdown":
			if not ctx.message.author.id == self.bot.config["discord"]["botMaster"]:
				await ctx.send("Access Denied.")
				return

			await ctx.send("Shutting Down")
			await ctx.bot.logout()
			
		elif subcommand == "disable":
			if not ctx.message.author.id in self.bot.config["discord"]["botControllers"] and not ctx.message.author.id == self.bot.config["discord"]["botMaster"]:
				await ctx.send("Access Denied. Please contact PeterCrawley if this should not be the case.")
				return

			self.bot.botController.disabled = True

			await ctx.send("Disabled")

		elif subcommand == "enable":
			if not ctx.message.author.id in self.bot.config["discord"]["botControllers"] and not ctx.message.author.id == self.bot.config["discord"]["botMaster"]:
				await ctx.send("Access Denied. Please contact PeterCrawley if this should not be the case.")
				return

			self.bot.botController.disabled = False

			await ctx.send("Enabled")

		else:
			await ctx.send("Invalid subcommand.")

def setup(bot):
	bot.add_cog(botControl(bot))
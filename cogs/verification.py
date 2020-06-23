from discord.ext import commands
import discord

import lib.verificationHandler as verificationHandler

class verification(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def verify(self, ctx, player):
		self.bot.botController.beginUsage()

		code = verificationHandler.createCode(player, ctx.message.author.id)

		await self.bot.botController.runCommand("/mail send " + player + " StarBot Verification Code: " + code + " The code will expire in 5 minutes.")

		self.bot.botController.endUsage()

		await ctx.send(f"A verification message has been sent to {player}. Please check your mail on creative and send the verification code to the bot via a Direct Message in discord.")

def setup(bot):
	bot.add_cog(verification(bot))

	@bot.event
	async def on_message(message):
		if message.channel == discord.DMChannel():
			print(message.content)
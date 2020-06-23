from discord.ext import commands
import discord

import lib.verificationHandler as verificationHandler

class verification(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def verify(self, ctx, playerOrCode = ""):
		if playerOrCode == "": return await ctx.send("Player name or verification code required")

		if len(playerOrCode) == 2:
			if verificationHandler.verifyCode(playerOrCode, ctx.message.author.id) == True:
				await ctx.send("Verified")

			else:
				await ctx.send("Verification code is invalid or incorrect.")

		else:
			self.bot.botController.beginUsage()

			code = verificationHandler.createCode(playerOrCode, ctx.message.author.id)

			await self.bot.botController.runCommand("/mail send " + playerOrCode + " StarBot Verification Code: " + code + " The code will expire in 5 minutes.")

			self.bot.botController.endUsage()

			await ctx.send(f"A verification message has been sent to {playerOrCode}. Please check your mail on creative and send the verification code to the bot via a Direct Message in discord.")

	@commands.command()
	async def unverify(self, ctx):
		verificationHandler.unverifyDiscord(ctx.message.author)

		await ctx.send("Removed all minecraft accounts associated with this account.")

def setup(bot):
	bot.add_cog(verification(bot))
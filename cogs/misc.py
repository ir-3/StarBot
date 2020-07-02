from discord.ext import commands

class misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx):
		await ctx.send("""**StarBot v2d1.0**

Commands:
>playerInfo (>playerinfo / >pi) : Gets details about a player
>nationInfo (>nationinfo / >ni) : Gets details about a nation
>nationTop (>nt / >ntop / >nationtop) : Nation Leaderboard
>settlementInfo (>settlementinfo / >si) : Gets details about a settlement
>settlementTop (>st / >stop / >settlementtop) : Settlement Leaderboard

Bot Discord Server: https://discord.gg/cPkrrrj""")

def setup(bot):
	bot.add_cog(misc(bot))
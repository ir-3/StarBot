from discord.ext import commands
import discord
import lib.nationColor as nationColor

class utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ["playerinfo", "pi"])
	async def playerInfo(self, ctx, player = ""):
		if self.bot.botController.disabled == True:
			return await ctx.send("Bot is currently disabled.")

		if player == "":
			await ctx.send("A player name is required.")
			return

		settlement = "Settlement: None"
		nation = "Nation: None"
		
		self.bot.botController.beginUsage()
		await self.bot.botController.runCommand(f"/pi {player}")

		while True:
			output = self.bot.botController.getLine()

			if output == -1:
				await ctx.send("Unable to establish or maintain connection to the server")
				return

			if output.startswith("Settlement: "): settlement = output
			elif output.startswith("Nation: "): nation = output
			elif output.startswith("SLXP: "): slxp = output
			elif output.startswith("Level: "): level = output         
			elif output.startswith("Last Seen: "):
				seen = output
				break
			elif output.startswith("Error: Player "):
				self.bot.botController.endUsage()
				await ctx.send(f"Player \"{player}\" not found.")
				return

		self.bot.botController.endUsage()

		settlement = settlement.replace("Settlement: ", "")
		nation = nation.replace("Nation: ", "")
		slxp = slxp.replace("SLXP:", "")
		level = level.replace("Level:", "")
		seen = seen.replace("Last Seen:", "")

		embed=discord.Embed(title=f"Player Info for {player}", color=nationColor.getNationColor(nation))
		embed.add_field(name="Settlement", value=settlement, inline=True)
		embed.add_field(name="Nation", value=nation, inline=True)
		embed.add_field(name="Experience", value=slxp, inline=True)
		embed.add_field(name="Level", value=level, inline=True)
		embed.add_field(name="Last Seen", value=seen, inline=True)
		embed.set_footer(text=f"Requested by {ctx.message.author.name}")
		await ctx.send(embed=embed)

	@commands.command(aliases = ["nationinfo", "ni"])
	async def nationInfo(self, ctx, nation = ""):			
		if self.bot.botController.disabled == True:
			return await ctx.send("Bot is currently disabled.")

		if nation == "":
			await ctx.send("A nation name is required.")
			return

		outposts = "Outposts (0): None"
		settlements = "Settlements (0): None"
		balance = "Balance: 0"
		leader = "Leader: None"
		membersHeader = "Members (0 Total, 0 Active, 0 Semi-Active, 0 Inactive)"
		members = "None"

		self.bot.botController.beginUsage()
		await self.bot.botController.runCommand(f"/n info {nation}")

		while True:
			output = self.bot.botController.getLine()

			if output == -1:
				await ctx.send("Unable to establish or maintain connection to the server")
				return

			if output.startswith("Outposts ("): outposts = output
			elif output.startswith("Settlements ("): settlements = output
			elif output.startswith("Balance: "): balance = output
			elif output.startswith("Leader: "): leader = output
			elif output.startswith("Members: "):
				membersHeader = output

				output = self.bot.botController.getLine()
				members = output
			elif output.startswith("=") and not leader == "Leader: None": break
			elif output.startswith("Error: Nation "):
				self.bot.botController.endUsage()
				await ctx.send(f"Nation \"{nation}\" not found.")
				return

		self.bot.botController.endUsage()

		membersHeader = membersHeader.replace(":", "")
		membersHeader = membersHeader.replace(") (", " Total, ")
		membersHeader = membersHeader.replace("ctive", "ctive,")
		membersHeader = membersHeader.replace("nactive,", "nactive")

		embed=discord.Embed(title=f"Nation Info for {nation}", color=nationColor.getNationColor(nation)) 
		embed.add_field(name=outposts.split("): ")[0]+")", value=outposts.split("): ")[1], inline=False)
		embed.add_field(name=settlements.split("): ")[0]+")", value=settlements.split("): ")[1], inline=False)
		embed.add_field(name="Balance", value=balance[8:], inline=True)
		embed.add_field(name="Leader", value=leader[7:], inline=True)
		embed.add_field(name=membersHeader, value=members, inline=False)
		embed.set_footer(text=f"Requested by {ctx.message.author.name}")
		await ctx.send(embed=embed)

	@commands.command(aliases = ["settlementinfo", "si"])
	async def settlementInfo(self, ctx, settlement = ""):
		if self.bot.botController.disabled == True:
			return await ctx.send("Bot is currently disabled.")

		if settlement == "":
			await ctx.send("A settlement name is required.")
			return

		nation = "Nation: None"
		territory = "Territory: None"
		balance = "Balance: 0"
		leader = "Leader: None"
		tradeCity = ""
		membersHeader = "Members (0 Total, 0 Active, 0 Semi-Active, 0 Inactive)"
		members = "None"

		self.bot.botController.beginUsage()
		await self.bot.botController.runCommand(f"/s info {settlement}")

		while True:
			output = self.bot.botController.getLine()

			if output == -1:
				await ctx.send("Unable to establish or maintain connection to the server")
				return

			if output.startswith("Nation: "): nation = output
			elif output.startswith("Territory: "): territory = output
			elif output.startswith("Balance: "): balance = output
			elif output.startswith("Leader: "): leader = output
			elif output.startswith("City State: "): tradeCity = "Trade City: "
			elif output.startswith("City Trade Tax: "): tradeCity += output.replace("City Trade Tax: ", "")
			elif output.startswith("Members: "):
				membersHeader = output

				output = self.bot.botController.getLine()
				members = output
			elif output.startswith("=") and not leader == "Leader: None": break
			elif output.startswith("Error: Settlement "):
				self.bot.botController.endUsage()
				await ctx.send(f"Settlement \"{settlement}\" not found.")
				return

		self.bot.botController.endUsage()

		nation = nation.split()
		nation = nation[0] + " " + nation[1]

		territory = territory.replace("North", "N")
		territory = territory.replace("East", "E")
		territory = territory.replace("South", "S")
		territory = territory.replace("West", "W")
		territory = territory.replace("north", "N")
		territory = territory.replace("east", "E")
		territory = territory.replace("south", "S")
		territory = territory.replace("west", "W")
		territory = territory.replace("Center", "C")

		membersHeader = membersHeader.replace(":", "")
		membersHeader = membersHeader.replace(") (", " Total, ")
		membersHeader = membersHeader.replace("ctive", "ctive,")
		membersHeader = membersHeader.replace("nactive,", "nactive")

		embed=discord.Embed(title=f"Settlement Info for {settlement}", color=nationColor.getNationColor(nation.split(": ")[1]))
		embed.add_field(name=nation.split(": ")[0], value=nation.split(": ")[1], inline=True)
		embed.add_field(name=territory.split(": ")[0], value=territory.split(": ")[1][:-1], inline=True)
		embed.add_field(name="Balance", value=balance[8:], inline=True)
		embed.add_field(name="Leader", value=leader[7:], inline=True)

		if not tradeCity == "":
			embed.add_field(name=tradeCity.split(": ")[0], value=tradeCity.split()[2] + " Tax", inline=True)

		embed.add_field(name=membersHeader, value=members, inline=False)
		embed.set_footer(text=f"Requested by {ctx.message.author.name}")
		await ctx.send(embed=embed)

	@commands.command(aliases = ["nt", "ntop", "nationtop"])
	async def nationTop(self, ctx, page = 1):
		if not isinstance(page, int):
			return await ctx.send("Page number must be an integer or blank.")
		if self.bot.botController.disabled == True:
			return await ctx.send("Bot is currently disabled.")

		ready = False
		outputArray = []

		self.bot.botController.beginUsage()
		await self.bot.botController.runCommand(f"/n top {page}")

		while True:
			output = self.bot.botController.getLine()

			if output.startswith("="):
				ready = not ready
				if not ready: break

			else:
				if ready:
					outputArray.append(output)

		self.bot.botController.endUsage()

		outputArray.pop(0)
		outputEnd = outputArray[-1].replace("/", " / ").replace("[<--] ", "").replace(" [-->]", " ")
		outputArray.pop(-1)

		output = "```markdown\n#Name / Leader / Members / Settlements / Outposts#"

		for nation in outputArray:
			nationInfoArray = nation.split(" ")
			output += f"\n{nationInfoArray[0]} / {nationInfoArray[1]} / {nationInfoArray[2]} {nationInfoArray[3]} {nationInfoArray[4]} {nationInfoArray[5]}{nationInfoArray[6]} / {nationInfoArray[7]} / {nationInfoArray[8]}"

		output += f"\n< {outputEnd}>```"

		await ctx.send(output)

	@commands.command(aliases = ["st", "stop", "settlementtop"])
	async def settlementTop(self, ctx, page = 1):
		if not isinstance(page, int):
			return await ctx.send("Page number must be an integer or blank.")
		if self.bot.botController.disabled == True:
			return await ctx.send("Bot is currently disabled.")

		ready = False
		outputArray = []

		self.bot.botController.beginUsage()
		await self.bot.botController.runCommand(f"/s top {page}")

		while True:
			output = self.bot.botController.getLine()

			if output.startswith("="):
				ready = not ready
				if not ready: break

			else:
				if ready:
					outputArray.append(output)

		self.bot.botController.endUsage()

		outputArray.pop(0)
		outputEnd = outputArray[-1].replace("/", " / ").replace("[<--] ", "").replace(" [-->]", " ")
		outputArray.pop(-1)

		output = "```markdown\n#Name / Leader / Members / Nation#"

		for settlement in outputArray:
			settlementInfoArray = settlement.split(" ")
			if not len(settlementInfoArray) == 8: settlementInfoArray.append("None")
			output += f"\n{settlementInfoArray[0]} / {settlementInfoArray[1]} / {settlementInfoArray[2]} {settlementInfoArray[3]} {settlementInfoArray[4]} {settlementInfoArray[5]}{settlementInfoArray[6]} / {settlementInfoArray[7]}"

		output += f"\n< {outputEnd}>```"

		await ctx.send(output)

def setup(bot):
	bot.add_cog(utils(bot))
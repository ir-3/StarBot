import subprocess, asyncio, json

config = json.loads(open("data/config.json", "r").read())

class botControllerClass:
	def __init__(self):
		self.active = False
		self.client = None
		self.timeRemaining = 0
		self.disabled = False

	def beginUsage(self):
		if self.active == False and self.timeRemaining <= 0 and self.disabled == False:
			self.active = True

			self.client = subprocess.Popen(["python3", "components/minecraft.py"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)

			while True:
				output = self.getLine()

				if output.find(" [+] ("):
					break
		
		self.client.stdout.flush()

	def getLine(self):
		output = str(self.client.stdout.readline().strip())[2:-1]

		self.client.poll()

		print(f"RECIVE: {output}")

		if output == "[HANDLER]CONNFAIL":
			self.client.stdout.flush()
			self.client.terminate()
			return -1

		if self.disabled == True:
			return -1

		return output

	async def runCommand(self, command):
		self.client.stdin.write(bytes(f"{command}\n", encoding="UTF-8"))
		try:		
			self.client.stdin.flush()
		except:
			del self.client
			self.active = False
			self.timeRemaining = 0
			self.beginUsage()
			await asyncio.sleep(1)
			self.client.stdin.write(bytes(f"{command}\n", encoding="UTF-8"))

		print(f"SEND: {command}")

	def endUsage(self):
		self.active = False
		self.timeRemaining = config["minecraft"]["connectionCooldown"]

	async def activeCheck(self):
		while True:
			if self.disabled == True:
				try:
					self.client.terminate()
				except:
					pass
				self.active = False
				self.client = None
				self.timeRemaining = 0

			if self.active == False:
				self.timeRemaining -= 1

			if self.timeRemaining <= 0:
				try:
					self.client.terminate()
				except:
					pass

			await asyncio.sleep(1)
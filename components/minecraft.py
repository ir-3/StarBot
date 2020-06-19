import os, sys, json

from twisted.internet import defer, reactor, stdio
from twisted.protocols import basic
from quarry.net.auth import Profile
from quarry.net.client import ClientFactory, SpawningClientProtocol

config = json.loads(open("data/config.json", "r").read())

class StdioProtocol(basic.LineReceiver):
	delimiter = os.linesep.encode('ascii')
	in_encoding  = getattr(sys.stdin,  "encoding", 'utf8')
	out_encoding = getattr(sys.stdout, "encoding", 'utf8')

	def lineReceived(self, line):
		self.minecraft_protocol.send_chat(line.decode(self.in_encoding))

	def send_line(self, text):
		self.sendLine(text.encode(self.out_encoding))

class MinecraftBotProtocol(SpawningClientProtocol):
	def packet_chat_message(self, buff):
		p_text = buff.unpack_chat().to_string()
		p_position = buff.unpack('B')

		if p_position in (0, 1) and p_text.strip():
			self.stdio_protocol.send_line(p_text)

	def send_chat(self, text):
		self.send_packet("chat_message", self.buff_type.pack_string(text))

class MinecraftBotFactory(ClientFactory):
	protocol = MinecraftBotProtocol

	def buildProtocol(self, addr):
		minecraft_protocol = super(MinecraftBotFactory, self).buildProtocol(addr)
		stdio_protocol = StdioProtocol()

		minecraft_protocol.stdio_protocol = stdio_protocol
		stdio_protocol.minecraft_protocol = minecraft_protocol

		stdio.StandardIO(stdio_protocol)
		return minecraft_protocol

	def clientConnectionLost(self, connector, reason):
		print("[HANDLER]CONNFAIL")

@defer.inlineCallbacks
def main():
	profile = yield Profile.from_credentials(str(config["minecraft"]["email"]), str(config["minecraft"]["password"]))
	factory = MinecraftBotFactory(profile)
	factory.connect(config["minecraft"]["serverAddress"])

main()
reactor.run()
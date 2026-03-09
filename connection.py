import asyncio
from conf import HOST, LISTENING_PORT, PEER_LISTENING_PORT, INTERFACE
from events import bus

class PeerConnection:
    def __init__(self):
        self.writer = None

        # Init bus
        bus.subscribe("outgoing_message", self.send)

    async def connect(self):
        reader, self.writer = await asyncio.open_connection(HOST, PEER_LISTENING_PORT)
        asyncio.create_task(self.receive_loop(reader, self.writer))

    async def receive_loop(self, reader, _writer):
        while True:
            data = await reader.read(1024)
            if not data:
                break
            
            bus.dispatch("message_received", data.decode())

    async def send(self, message):
        if self.writer:
            self.writer.write(message.encode())
            await self.writer.drain()

    async def start_server(self):
        """Start a listening server for incoming connections."""
        server = await asyncio.start_server(self.receive_loop, INTERFACE, LISTENING_PORT)
        async with server:
            await server.serve_forever()

import asyncio
import ui
from connection import PeerConnection

peer = PeerConnection()

async def main():
    # Start server to listen for incoming messages
    asyncio.create_task(peer.start_server())

    await asyncio.sleep(3)

    # Connect to peer to send messages
    await peer.connect()

    await ui.main()


if __name__ == "__main__":
    asyncio.run(main())

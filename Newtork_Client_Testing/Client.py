import asyncio
from websockets.asyncio.client import connect


async def hello(msg: str):
    async with connect("ws://10.251.141.83:13") as websocket:
        await websocket.send(msg)
        message = await websocket.recv()
        print(message)


if __name__ == "__main__":
    while True:
        asyncio.run(hello(input("Vad vill du skicka till servern")))
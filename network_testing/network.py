from websockets.asyncio.server import serve
import asyncio

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
    

async def main():
    async with serve(echo, "localhost", 14) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
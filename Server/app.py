import asyncio
import websockets


connected = set()


async def server(websocket):
    connected.add(websocket)
    try:
        if len(connected) < 5:
            await websocket.send("Insufficient users")
    finally:
        connected.remove(websocket)


# async def main():
#     async with websockets.serve(server, "localhost", 8765):
#         await asyncio.Future()  # run forever


# asyncio.run(main())


start_server = websockets.serve(server, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
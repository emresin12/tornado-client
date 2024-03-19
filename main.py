import time

from tornado import websocket
import asyncio

url = "ws://127.0.0.1:8888"


async def latency_test():
    for i in range(100):
        conn = await websocket.websocket_connect(url)
        start_time = time.time()
        await conn.write_message("x")
        message = await conn.read_message()
        print(f"Received message: {message}")
        end_time = time.time()
        print(f"Latency: {end_time - start_time} seconds")


async def listen(conn):
    while True:
        message = await conn.read_message()
        if message is None:  # Connection closed
            break
        # print(f"Received message: {message}")

async def connect_and_listen(i):
    try:
        conn = await websocket.websocket_connect(url)
        print("connected to server " + str(i))
        await listen(conn)
        time.sleep(0.01)
    except Exception as e:
        print(f"Connection {i} failed: {e}")

async def main():
    tasks = [connect_and_listen(i) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())

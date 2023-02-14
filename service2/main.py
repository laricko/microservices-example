import asyncio
import json

import aio_pika
from aio_pika import Channel, Message, Queue


QUEUE_NAME_TO_SECOND_SERVICE = "changebalance_orders"


async def get_queue(channel: Channel) -> Queue:
    return await channel.declare_queue(QUEUE_NAME_TO_SECOND_SERVICE)


async def change_balance(message: Message):
    """
    Logic service
    """
    async with message.process():
        data = json.loads(message.body.decode())
        user = data.get("user_id")
        print(f"[*] - User's balance with id {user} changed. Order checkouted")


async def main() -> None:
    connection = await aio_pika.connect(host="rabbitmq")
    channel: Channel = await connection.channel()
    queue = await get_queue(channel)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await change_balance(message)


if __name__ == "__main__":
    print("SERVICE 2 STARTED...")
    asyncio.run(main())

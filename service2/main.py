import asyncio
import logging
import json

import aio_pika
from aio_pika import Channel, Message
from aio_pika.exceptions import ChannelNotFoundEntity


QUEUE_NAME_TO_SECOND_SERVICE = "change_balance"


async def get_queue(channel):
    try:
        queue = await channel.get_queue(QUEUE_NAME_TO_SECOND_SERVICE, ensure=True)
    except ChannelNotFoundEntity:
        queue = await channel.declare_queue(QUEUE_NAME_TO_SECOND_SERVICE, durable=True)
    return queue


async def change_balance(message: Message):
    data = json.loads(message.body.decode())
    user = data.get("user_id")
    print(f"[*] - User's balance with id {user} changed")


async def main() -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel: Channel = await connection.channel()
    queue = await get_queue(channel)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await change_balance(message)


if __name__ == "__main__":
    asyncio.run(main())

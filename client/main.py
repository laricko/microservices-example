import json

import uvicorn
import pika
from fastapi import FastAPI
from aio_pika import connect_robust, Channel, Message
from aio_pika.exceptions import ChannelNotFoundEntity


EXCHANGER = "amq.direct"
ROUTING_KEY = "order.created"

QUEUE_NAME_TO_FIRST_SERVICE = "notify_user"
QUEUE_NAME_TO_SECOND_SERVICE = "change_balance"


app = FastAPI()


foo_data = {
    "id": 50,
    "user_id": 12,
    "title": "Hello world",
    "description": """Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
    when an unknown printer took a galley of type and scrambled it to make a type specimen book.""",
    "category_id": 4,
    "price": "5000",
}


@app.get("/sync-endpoint")
def sync_endpoint():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_bind(QUEUE_NAME_TO_FIRST_SERVICE, "amq.direct", ROUTING_KEY)
    channel.basic_publish(EXCHANGER, ROUTING_KEY, json.dumps(foo_data).encode())
    return {"detail": "User subscribed."}


async def async_connect_to_broker() -> Channel:
    a_connection = await connect_robust("amqp://guest:guest@localhost/")
    return await a_connection.channel()


@app.get("/async-endpoint")
async def async_endpoint():
    connection = await connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    exchange = await channel.get_exchange(EXCHANGER)
    try:
        queue = await channel.get_queue(QUEUE_NAME_TO_SECOND_SERVICE)
    except ChannelNotFoundEntity:
        queue = await channel.declare_queue(QUEUE_NAME_TO_SECOND_SERVICE, durable=True)
    await queue.bind(exchange, ROUTING_KEY)
    message = Message(json.dumps(foo_data).encode(), content_type="application/json")
    await exchange.publish(message, ROUTING_KEY)
    return {"detail": "Order created."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)

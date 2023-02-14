import json

import uvicorn
import pika
from fastapi import FastAPI
from aio_pika import Message, connect
from aio_pika.exceptions import ChannelNotFoundEntity


EXCHANGER = "amq.direct"
ROUTING_KEY_TO_FIRST_SERVICE = "user.mailing"
ROUTING_KEY_TO_SECOND_SERVICE = "orders.checkout"

QUEUE_NAME_TO_FIRST_SERVICE = "notify_user"
QUEUE_NAME_TO_SECOND_SERVICE = "changebalance_orders"


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


@app.post("/api/user/subscribe")
def subscribe_user():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_bind(
        QUEUE_NAME_TO_FIRST_SERVICE, "amq.direct", ROUTING_KEY_TO_FIRST_SERVICE
    )
    channel.basic_publish(
        EXCHANGER, ROUTING_KEY_TO_FIRST_SERVICE, json.dumps(foo_data).encode()
    )
    return {"detail": "User subscribed."}


@app.post("/api/order/checkout")
async def order_checkout():
    connection = await connect(host="rabbitmq")
    channel = await connection.channel()
    exchange = await channel.get_exchange(EXCHANGER)
    try:
        queue = await channel.get_queue(QUEUE_NAME_TO_SECOND_SERVICE)
    except ChannelNotFoundEntity:
        queue = await channel.declare_queue(QUEUE_NAME_TO_SECOND_SERVICE, durable=True)
    await queue.bind(exchange, ROUTING_KEY_TO_SECOND_SERVICE)
    message = Message(json.dumps(foo_data).encode(), content_type="application/json")
    await exchange.publish(message, ROUTING_KEY_TO_SECOND_SERVICE)
    return {"detail": "Order created."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

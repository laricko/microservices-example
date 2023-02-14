import json

import pika


QUEUE_NAME_TO_FIRST_SERVICE = "notify_user"


def notify_user(ch, method, properties, data):
    """
    Logic service
    """
    data = json.loads(data.decode())
    user = data.get("user_id")
    print(f"[*] - User with id {user} just notified. And subscribed")


if __name__ == "__main__":
    print("SERVICE 1 STARTED...")
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    queue = channel.queue_declare(QUEUE_NAME_TO_FIRST_SERVICE)
    channel.basic_consume(QUEUE_NAME_TO_FIRST_SERVICE, notify_user)
    channel.start_consuming()

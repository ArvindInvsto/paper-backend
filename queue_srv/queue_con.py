# from BasePikaCon import BasicPikaClient


import ssl
import pika

class BasicPikaClient:

    def __init__(self, rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, region):

        # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671"
        parameters = pika.URLParameters(url)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
class BasicMessageSender(BasicPikaClient):

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        # print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")
        print(f"Sent message. Exchange: {exchange}")
    def close(self):
        self.channel.close()
        self.connection.close()


"""

if __name__ == "__main__":

    # Initialize Basic Message Sender which creates a connection
    # and channel for sending messages.
    basic_message_sender = BasicMessageSender(
        "b-ec80e0b6-25ca-4a5e-82f1-8d1c3929eecf",
        "invsto",
        "invsto@12345",
        "us-east-2"
    )

    # Declare a queue
    # basic_message_sender.declare_queue("hello akshar ! (python)")


    body_ = {
    "userid":'akshar',
    "order_id":'10223',
    "trading_symbol":'NIFTYFUT',
    "qty":50,
    "exchange":'NFO',
    "trans_type":'BUY"',
    "timestamp":"2023-03-05 13:00:00",
    "product":'FUT',
    "order_type":'MKT"',
    "price":18010.05,
    "stoploss_trigger":17910.05,
    "status":'ACTIVE'
    }
    # Send a message to the queue.

    basic_message_sender.send_message(exchange="sharksigma", routing_key="invsto", body=str(body_))

    # Close connections.
    basic_message_sender.close()
    """
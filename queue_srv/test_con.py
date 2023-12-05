from queue_con import RabbitmqConfigure,RabbitMq



if __name__ == "__main__":
    server = RabbitmqConfigure(queue='sharksigma',
                               host='https://b-ec80e0b6-25ca-4a5e-82f1-8d1c3929eecf.mq.us-east-2.amazonaws.com',
                               routingKey='invsto',
                               exchange='sharksigma')

    rabbitmq = RabbitMq(server)
    rabbitmq.publish(payload={"Data":22})

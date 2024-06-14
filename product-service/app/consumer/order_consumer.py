


from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

from app.deps import get_session
from app.crud.product_crud import verify_product_by_id





async def consumer_order_messages(topic,bootstrap_servers,group_id):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id
    )

    await consumer.start()

    try:
        async for message in consumer:
            print("RAW")
            print(f"Received message on topic {message.topic}")
            order_data = json.loads(message.value.decode())
            print("TYPE", (type(order_data)))
            print(f"Product Data {order_data}")

            with next(get_session()) as session:
                print(f"product order consumer messages check for order product is valid or not")

                is_verified = verify_product_by_id(product_id=order_data['product_id'],session=session)

                if is_verified is not None:
                    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
                    await producer.start()
                    try:
                        await producer.send_and_wait("product-order-event-verify",message.value)
                    finally:
                        await producer.stop()

                



    

    except Exception as e:
        print(e)

    finally:
        await consumer.stop()
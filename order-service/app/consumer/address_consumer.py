from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json  


from app.deps import get_session,get_kafka_producer
from app.crud.order_crud import create_address
from app.models.order_model import Address

async def consume_address_messages(topic,bootstrap_servers,group_id):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        # auto_offset_reset="earliest",
    )
    print(f"life span send topic:{topic}")
    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("RAW")
            print(f"Received message on topic {message.topic}")

            order_data = json.loads(message.value.decode())
            # print("TYPE", (type(order_data)))
            print(f"Data {order_data}")
            
            with next(get_session()) as session:
                print("SAVING Address DATA TO DATABSE")
                db_insert_address = create_address(
                    address_data=Address(**order_data), session=session)
                print("DB_INSERT_PRODUCT", db_insert_address)
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

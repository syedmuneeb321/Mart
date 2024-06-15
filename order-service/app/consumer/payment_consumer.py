from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json 

from app.utils.encode_and_decode import custom_decoder
from app.deps import get_session,get_kafka_producer
from app.crud.order_crud import verify_order

async def payment_varify_consumer(topic,bootstrap_servers,group_id):
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

            order_data = json.loads(message.value.decode(),object_hook=custom_decoder)
            # print("TYPE", (type(order_data)))
            
            print(f"Data {order_data}")
            # print(f"id type check on order consumer: {type(order_data['id'])}")
            
            with next(get_session()) as session:
                print("check payment order exist or not")
                order_veriefied = verify_order(
                    order_id=order_data['order_id'], session=session)
                if order_veriefied is not None:
                    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
                    await producer.start()
                    try:
                        await producer.send_and_wait("order-topic-response",message.value)
                    finally:
                        await producer.stop()
                else:
                    print(f"this order id {order_data['order_id']} not exist")    
    except Exception as e:
        print(f"error occured: {e}")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
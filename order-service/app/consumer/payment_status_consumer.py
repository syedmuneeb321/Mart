from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json 

from app.utils.encode_and_decode import custom_decoder
from app.deps import get_session,get_kafka_producer
from app.crud.order_crud import order_peyment_update
from app.models.order_model import PaymentStatus

async def payment_status_messages_consume(topic,bootstrap_servers,group_id):
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
            
            
            with next(get_session()) as session:
                print("payment status update")
                payment_completed = order_peyment_update(
                    order_id=order_data['order_id'],order_payment_status=PaymentStatus.paid,session=session)
                
              
    except Exception as e:
        print(f"error occured: {e}")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
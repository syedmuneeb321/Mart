from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json


from app.models.product_model import Product, ProductUpdate
from app.crud.product_crud import add_new_product, get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id,verify_product_by_id
from app.deps import get_session, get_kafka_producer




async def consume_inventory_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="consumer-inventory-group-validation",
        # auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("Raw")
            print(f"Received message on topic {message.topic}")

            product_data = json.loads(message.value.decode())
            print("TYPE", (type(product_data)))
            print(f"Product Data {product_data}")

            product_id = product_data['product_id']
                

            with next(get_session()) as session:
                print("check product by id")
                product_varified = verify_product_by_id(
                    product_id=product_id, session=session)

                print("DB_verified_PRODUCT", product_varified)
                if product_varified is not None:
                    print("PRODUCT VALIDATION CHECK NOT NONE")

                    producer=AIOKafkaProducer(bootstrap_servers='broker:19092')
                    await producer.start()
                    try:
                        await producer.send_and_wait("inventory-add-stock-response",message.value) 

                    finally:
                        await producer.stop() 
                else:
                    print(f"")
                

                    

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

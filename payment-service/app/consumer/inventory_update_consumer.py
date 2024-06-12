




from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
from typing import List

from app import settings
from app.db_engine import engine
from app.models.inventory_model import InventoryItems,InventoryItems
from app.crud.inventory_crud import create_inventory_item,get_all_inventories,inventory_update
from app.deps import get_session, get_kafka_producer
from uuid import UUID

async def consume_update_messages(topic, bootstrap_servers,group_id):
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
            print("TYPE", (type(order_data)))
            print(f"Data {order_data}")
            
            # # print(f"inventory data id type: {type(order_data['id'])}")
            item_id = UUID(order_data['id'])
            # print(item_id)
            items = order_data['item']
            # print(items)
            with next(get_session()) as session:
                db_insert_inventory = inventory_update(item_id=item_id,
                    item=InventoryItems(**items), session=session)
            
    except Exception as e:
        print(e)
            
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
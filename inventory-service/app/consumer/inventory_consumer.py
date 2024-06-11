from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
from typing import List

from app import settings
from app.db_engine import engine
from app.models.inventory_model import InventoryItems
from app.crud.inventory_crud import create_inventory_item,get_all_inventories
from app.deps import get_session, get_kafka_producer
from uuid import UUID

async def consume_messages(topic, bootstrap_servers,group_id):
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
            
            # print(f"inventory data id type: {type(order_data['id'])}")
            order_data['id'] = UUID(order_data['id'])
            
            # print(type(order_data['id']))
            # print(order_data['id'])
            data = InventoryItems(**order_data)
            # print(data.id)
            with next(get_session()) as session:
                db_insert_inventory = create_inventory_item(
                    item=data, session=session)
            
    except Exception as e:
        print(e)
            
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
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
# from app.db_engine import engine
# from app.models.inventory_model import InventoryItems
# from app.crud.inventory_crud import create_inventory_item,get_all_inventories
from app.deps import  get_kafka_producer
from uuid import UUID
from app.utils.utils import send_email,get_user_by_id

async def consume_payment_status_message(topic, bootstrap_servers,group_id):
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

            payment_data = json.loads(message.value.decode())
            # print("TYPE", (type(order_data)))
            print(f"Data {payment_data}")
            print(f"user data: {get_user_by_id(customer_id=payment_data['customer_id'])},{type(get_user_by_id(customer_id=payment_data['customer_id']))}")
            user_data = get_user_by_id(customer_id=payment_data['customer_id'])
            # print(f"inventory data id type: {type(order_data['id'])}")
            email_to = user_data['email']
            email_content= f"dear {user_data['user_name']} order payment is successfully paid"
            email_subject = "order payment paid"
            send_email(email_to=email_to,subject=email_subject,email_content_for_send=email_content)
            
           
    except Exception as e:
        print(e)
            
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
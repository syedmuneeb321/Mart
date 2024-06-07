# main.py
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

from app import settings
from app.db_engine import engine
from app.models.order_model import Address,Order
from app.crud.order_crud import create_address
from app.deps import get_session, get_kafka_producer

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        # auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("RAW")
            print(f"Received message on topic {message.topic}")

            order_data = json.loads(message.value.decode())
            print("TYPE", (type(order_data)))
            print(f"User Data {order_data}")

            with next(get_session()) as session:
                print("SAVING DATA TO DATABSE")
                # db_insert_product = create_user(
                #     user_data=UserCreate(**user_data), session=session)
                # print("DB_INSERT_PRODUCT", db_insert_product)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating table!")

    task = asyncio.create_task(consume_messages(
        settings.KAFKA_ORDER_TOPIC, 'broker:19092'))
    task = asyncio.create_task(consume_messages(
        "address-topic", 'broker:19092'))
    
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)



@app.get("/")
def read_root():
    return {"Hello": "order Service"}


@app.post("/add-address/", response_model=Address)
async def generate_address(address: Address, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    """ Create a new product and send it to Kafka"""
    
    address_dict = {field: getattr(address, field) for field in address.dict()}
   
    address_json = json.dumps(address_dict).encode("utf-8")
    
    print("product_JSON:", address_json)
    # Produce message
    await producer.send_and_wait("address-topic", address_json)
    
    return address


@app.post("/create-order/")
async def order_generate(order: Order, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    """ Create a new product and send it to Kafka"""
    
    order_dict = {field: getattr(order, field) for field in order.dict()}
   
    order_json = json.dumps(order_dict).encode("utf-8")
    
    print("product_JSON:", order_json)
    # Produce message
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_json)
    
    return order


# @app.get("/manage-products/{product_id}", response_model=Product)
# def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
#     """ Get a single product by ID"""
#     try:
#         return get_product_by_id(product_id=product_id, session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/manage-products/{product_id}", response_model=dict)
# def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    
    
#     """ Delete a single product by ID"""
#     try:
#         return delete_product_by_id(product_id=product_id, session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.patch("/manage-products/{product_id}", response_model=Product)
# def update_single_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
#     """ Update a single product by ID"""
#     try:
#         return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
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
# from app.models.user_model import User,UserPublic,UserCreate #ProductUpdate
# from app.crud.user_crud import create_user,user_login
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

            user_data = json.loads(message.value.decode())
            print("TYPE", (type(user_data)))
            print(f"User Data {user_data}")

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
    # create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)



@app.get("/")
def read_root():
    return {"Hello": "order Service"}


# @app.post("/register-user/", response_model=UserPublic)
# async def create_new_product(user: UserCreate, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
#     """ Create a new product and send it to Kafka"""
    
#     # product_dict = {field: getattr(user, field) for field in product.dict()}
#     user_dict = user.__dict__
#     user_json = json.dumps(user_dict).encode("utf-8")
#     print("product_JSON:", user_json)
#     # Produce message
#     await producer.send_and_wait(settings.KAFKA_USER_TOPIC, user_json)
#     # new_product = add_new_product(product, session)
#     return user 

# @app.post("/user-login",response_model=UserPublic)
# def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)],session: Annotated[Session, Depends(get_session)]):
#     """ Get all products from the database"""
#     user = user_login(form_data=form_data,session=session)
#     return user

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
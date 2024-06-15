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
# from app.db_engine import engine
from app.models.user_model import User,UserPublic,UserTokenPublic,UserCreate #ProductUpdate
# from app.crud.user_crud import create_user,user_login,role_assign_by_admin,CurrentUser,get_all_users,update_user
from app.deps import get_kafka_producer
from app.consumer.product_consumer import consume_product_messages
from app.consumer.order_consumer import consume_order_messages
from app.consumer.payment_status_consumer import consume_payment_status_message
from app.consumer.order_status_consumer import consume_order_status_messages

# def create_db_and_tables() -> None:
#     SQLModel.metadata.create_all(engine)




# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Notification serive")

    product_task = asyncio.create_task(consume_product_messages( "product-events", 'broker:19092',"product-event-consumer-group-for-notfication"))
    order_task = asyncio.create_task(consume_order_messages("product-order-event-verify", 'broker:19092',"order-event-consumer-group-for-notfication"))
    payment_status_task = asyncio.create_task(consume_payment_status_message("payment-status-topic", 'broker:19092',"order-payment-status-consumer-group-for-notfication"))
    order_status_task = asyncio.create_task(consume_order_status_messages("order-status-event", 'broker:19092',"order-status-consumer-group-for-notfication"))


    
    # create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="NOTIFICATION SERVICE API",
    version="0.0.1",
)



@app.get("/")
def read_root():
    return {"Hello": "Notification Service"}


# @app.post("/register-user/", response_model=UserPublic)
# async def create_new_product(user: UserCreate, session: DBSessionDep):
#     """ Create a new product and send it to Kafka"""
    
#     return create_user(user_data=user,session=session)
    
    

# @app.post("/user-login")
# def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)],session: Annotated[Session, Depends(get_session)]):
#     """ Get all products from the database"""
#     user = user_login(form_data=form_data,session=session)
#     return user

# @app.post("/role-assign/", response_model=UserPublic)
# def get_single_product(user_data:UserCreate,session:DBSessionDep):
#     """ Get a single product by ID"""
#     try:
#         return role_assign_by_admin(user_data=user_data,session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.get('/user/me',response_model=UserPublic)
# async def get_user_me(user:CurrentUser):
#     return user

# @app.get('/token-verify',response_model=UserTokenPublic)
# async def token_verify(user:CurrentUser):
#     return user


# @app.get("/get-all-user",response_model=list[UserPublic])
# def all_user(users:Annotated[UserPublic,Depends(get_all_users)]):
#     return users

# @app.patch("/user-update/",response_model=UserPublic)
# def user_update(user: Annotated[UserPublic, Depends(update_user)]):
#     """ Update a single user inforamtion like email etc."""
#     try:
#         return user
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





    

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
from app.models.order_model import Address,CreateUserAddress,UpdateAddress,CreateOrder,Order,OrderStatus,PaymentStatus
from app.crud.order_crud import create_address,create_order,get_customer_orders,order_status_update,order_peyment_update
from app.crud.order_crud import get_address,update_address,delete_address
from app.deps import get_session,LoginForAccessTokenDep,GetCurrentUserDep,DBSessionDep,ProducerDep

from app.consumer.payment_consumer import payment_varify_consumer
from app.consumer.address_consumer import consume_address_messages
from app.consumer.order_consumer import consume_product_order_messages
from app.consumer.payment_status_consumer import payment_status_messages_consume

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)







# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating table...")

    order_task = asyncio.create_task(consume_product_order_messages(
        "product-order-event-verify", 'broker:19092',"order-group"))
    address_task = asyncio.create_task(consume_address_messages(
        "address-topic", 'broker:19092',"address-group"))
    verify_payment_task = asyncio.create_task(payment_varify_consumer(
        "payment-event", 'broker:19092',"payment-verify-group"))
    payment_status_task  = asyncio.create_task(payment_status_messages_consume(
        "payment-status-topic", 'broker:19092',"payment-status-consumer-group"))
    
    
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


@app.post("/auth/login")
def login(token:LoginForAccessTokenDep):
    return token

# @app.get("/current-user")
# def current_user(user:GetCurrentUserDep):
#     return user


@app.post("/add-address/")
async def generate_address(address: CreateUserAddress, session:DBSessionDep,user:GetCurrentUserDep):
    """ Create a new product and send it to Kafka"""
    print(user['id'])
    user_address = Address.model_validate(address,update={"user_id":user['id']})
    # print(user_address)
    return create_address(address_data=user_address,session=session)
    # return user_address


    # address_dict = {field: getattr(address, field) for field in address.dict()}
   
    # address_json = json.dumps(address_dict).encode("utf-8")
    
    # print("address_JSON:", address_json)
    # # Produce message
    # await producer.send_and_wait("address-topic", address_json)
    
    # return address


@app.get("/get-address/")
def get_user_address(session: DBSessionDep,user:GetCurrentUserDep):
    """ Get a single product by ID"""
    try:
        return get_address(id=user['id'], session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/update-address")
def update_user_address(address_id:int,address:UpdateAddress ,user:GetCurrentUserDep,session:DBSessionDep):
    
    
    try:
        return update_address(address_id=address_id,user_id=user['id'],address=address,session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete-address")    
def delete_user_address(address_id:int,user:GetCurrentUserDep,session:DBSessionDep):
    try:
       return delete_address(address_id=address_id,user_id=user['id'],session=session)
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")



@app.post("/create-order/")
async def order_generate(order:CreateOrder,user:GetCurrentUserDep, session: DBSessionDep, producer:ProducerDep):
    """ Create a new product and send it to Kafka"""
    if user:
        
        order_data = Order.model_validate(order,update={'customer_id':user['id']})
        order_dict = {field: getattr(order_data, field) for field in order_data.dict()}
        order_json = json.dumps(order_dict).encode("utf-8")
    
        print("order_JSON:", order_json)
    # Produce message
        await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_json)
    
        return order_dict


@app.get("/my-orders/")
def get_orders(session: DBSessionDep,user:GetCurrentUserDep):
    """ Get a single product by ID"""
    try:
        return get_customer_orders(customer_id=user['id'], session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






@app.patch("/update-order-status")
def update_order_status(order_id:int,user_id:int,order_status:OrderStatus,user:GetCurrentUserDep,session: DBSessionDep):
    if user['role'] == 'admin':
        try:
            return order_status_update(order_id=order_id,user_id=user_id,order_status=order_status,session=session)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    else:
        raise HTTPException(status_code=403,detail="not autherize for update status")
        

        

@app.patch("/cancel-order")
def order_cancel(order_id:int,user:GetCurrentUserDep,session:DBSessionDep):
    try:
        order_status=OrderStatus.cancelled
        return order_status_update(order_id=order_id,user_id=user['id'],order_status=order_status,session=session)
    except HTTPException as e:
        raise  e 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

    

# @app.patch("/update-payment-status")
# def update_payment_status(order_id:int,payment_status:PaymentStatus,session: Annotated[Session, Depends(get_session)]):

#     try:
#         return order_peyment_update(order_id=order_id,order_payment_status=payment_status,session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
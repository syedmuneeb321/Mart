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
from app.models.order_model import Address,Order,OrderStatus,PaymentStatus
from app.crud.order_crud import create_address,create_order,get_customer_orders,order_status_update,order_peyment_update
from app.deps import get_session, get_kafka_producer

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


# async def consume_address(topic,bootstrap_servers,group_id):
#     # Create a consumer instance.
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id=group_id,
#         # auto_offset_reset="earliest",
#     )
#     print(f"life span send topic:{topic}")
#     # Start the consumer.
#     await consumer.start()
#     try:
#         # Continuously listen for messages.
#         async for message in consumer:
#             print("RAW")
#             print(f"Received message on topic {message.topic}")

#             order_data = json.loads(message.value.decode())
#             # print("TYPE", (type(order_data)))
#             print(f"Data {order_data}")
            
#             with next(get_session()) as session:
#                 print("SAVING Address DATA TO DATABSE")
#                 db_insert_address = create_address(
#                     address_data=Address(**order_data), session=session)
#                 print("DB_INSERT_PRODUCT", db_insert_address)
#     finally:
#         # Ensure to close the consumer when done.
#         await consumer.stop()



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
            
            # with next(get_session()) as session:
            #     print("SAVING Address DATA TO DATABSE")
            #     db_insert_address = create_address(
            #         address_data=Address(**order_data), session=session)
            #     print("DB_INSERT_PRODUCT", db_insert_address)

            

            with next(get_session()) as session:
                if message.topic == "order-event":
                    print("SAVING order DATA TO DATABSE ")

                    # db_insert_order = create_order(
                    #     order_data=Order(**order_data), session=session)
                else:
                    print("SAVING address DATA TO DATABSE ")

                    # db_insert_address = create_address(
                    #     address_data=Address(**order_data), session=session)

                    # print("DB_INSERT_PRODUCT", db_insert_order)

            
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating table!")

    order_task = asyncio.create_task(consume_messages(
        "order-events", 'broker:19092',"order-group"))
    address_task = asyncio.create_task(consume_messages(
        "address-topic", 'broker:19092',"address-group"))
    
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
    
    print("address_JSON:", address_json)
    # Produce message
    await producer.send_and_wait("address-topic", address_json)
    
    return address


@app.post("/create-order/")
async def order_generate(order: Order, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    """ Create a new product and send it to Kafka"""
    
    order_dict = {field: getattr(order, field) for field in order.dict()}
   
    order_json = json.dumps(order_dict).encode("utf-8")
    
    print("order_JSON:", order_json)
    # Produce message
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_json)
    
    return order


@app.get("/my-orders/")
def get_orders(customer_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single product by ID"""
    try:
        return get_customer_orders(customer_id=customer_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/update-order-status")
def update_order_status(order_id:int,order_status:OrderStatus,session: Annotated[Session, Depends(get_session)]):

    try:
        return order_status_update(order_id=order_id,order_status=order_status,session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@app.patch("/update-payment-status")
def update_payment_status(order_id:int,payment_status:PaymentStatus,session: Annotated[Session, Depends(get_session)]):

    try:
        return order_peyment_update(order_id=order_id,order_payment_status=payment_status,session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@app.patch("/cancel-order")
def order_cancel(order_id:int,session: Annotated[Session, Depends(get_session)]):
    try:
        order_status:OrderStatus.cancelled
        return order_status_update(order_id=order_id,order_status=order_status,session=session)
    except HTTPException as e:
        e 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

    

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
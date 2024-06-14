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
from typing import List

from app import settings
from app.db_engine import engine
from app.models.payment_model import Payment,PaymentCreate,PaymentStatus,PaymentPublic 
from app.crud.payment_crud import payment_status_update
from app.deps import get_session, get_kafka_producer,DBSessionDep,ProducerDep,LoginForAccessTokenDep,GetCurrentUserDep
from datetime import datetime
from app.utils.encode_and_decode import CustomJSONEncoder,custom_decoder
from app.consumer.payment_consumer import payment_consume_messages
# from app.consumer.inventory_update_consumer import consume_update_messages




import json
from uuid import UUID





def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)








# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")

    payment_task = asyncio.create_task(payment_consume_messages(
        topic="order-topic-response", bootstrap_servers='broker:19092',group_id="payment_consumer_group"))
    # update_invetory_task = asyncio.create_task(consume_update_messages(
    #     topic="update-inventory-event", bootstrap_servers='broker:19092',group_id="consumer-update-group-id"))
  
    
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)



@app.get("/")
def read_root():
    return {"Hello": "payment service"}


@app.post("/auth/login")
def login(token:LoginForAccessTokenDep):
    return token




@app.post("/order-payment")
async def order_payment(payment: PaymentCreate,user:GetCurrentUserDep,producer: ProducerDep):
    """ Create a new inventory and send it to Kafka"""
    try:
        payment_data = Payment.model_validate(payment,update={"customer_id":user['id']})
        payment_dict = {field: getattr(payment_data, field) for field in payment_data.dict()}
        payment_json = json.dumps(payment_dict,cls=CustomJSONEncoder).encode("utf-8")
        print("payment_JSON:", payment_json)
        
        
        # Produce message
        await producer.send_and_wait(settings.KAFKA_PAYMENT_TOPIC, payment_json)
    
        return payment_dict
    except Exception as e:
        print(e)
    
    

@app.patch("/payment-status")
async def payment_status(payment_id:UUID,payment_status:PaymentStatus,session: Annotated[Session, Depends(get_session)],producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):

    try: 
        payment_info = payment_status_update(item_id=payment_id,payment_status=payment_status,session=session)
        if payment_info.payment_status == PaymentStatus.COMPLETED:
            payment_dict = {"order_id":payment_info.order_id,"payment_status":payment_info.payment_status}
            payment_json = json.dumps(payment_dict).encode("utf-8")
            await producer.send_and_wait("payment-status-topic",payment_json)
            
        return payment_info
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise e






# @app.get("/all-inventory/",response_model=List[InventoryItems])
# def get_all_inventory(session: Annotated[Session, Depends(get_session)]):
#     """ Get all inventory items"""
#     try:
#         return get_all_inventories(session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# @app.patch("/update-inventory")
# async def update_inventory(inventory_id:UUID,item:InvetoryItemsUpdate,producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):



#     try:
#         inventory_dict = {"id":str(inventory_id),"item":item.dict()}
#         inventory_json = json.dumps(inventory_dict).encode("utf-8")
#         print("producer > inventory json:",inventory_json)
#         await producer.send_and_wait("update-inventory-event",inventory_json)
#         # return inventory_update(item_id=inventory_id,item=item,session=session)
#         return item
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.delete("/delete-item/", response_model=dict)
# def detele_item(item_id:UUID, session: Annotated[Session, Depends(get_session)]):
#     """ Delete a single iventory item by ID"""
#     try:
#         return delete_invetory_item(item_id=item_id, session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

        


# @app.patch("/update-payment-status")
# def update_payment_status(order_id:int,payment_status:PaymentStatus,session: Annotated[Session, Depends(get_session)]):

#     try:
#         return order_peyment_update(order_id=order_id,order_payment_status=payment_status,session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
        

# @app.patch("/cancel-order")
# def order_cancel(order_id:int,session: Annotated[Session, Depends(get_session)]):
#     try:
#         order_status:OrderStatus.cancelled
#         return order_status_update(order_id=order_id,order_status=order_status,session=session)
#     except HTTPException as e:
#         e 
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=str(e))

    


    
# @app.patch("/manage-products/{product_id}", response_model=Product)
# def update_single_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
#     """ Update a single product by ID"""
#     try:
#         return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
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
from app.models.inventory_model import InventoryItems
from app.crud.inventory_crud import create_inventory_item,get_all_inventories
from app.deps import get_session, get_kafka_producer
from app.consumer.inventory_consumer import consume_messages



import json
from uuid import UUID

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)




def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)








# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables...")

    inventory_task = asyncio.create_task(consume_messages(
        topic="inventory-add-stock-response", bootstrap_servers='broker:19092',group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY))
  
    
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)



@app.get("/")
def read_root():
    return {"Hello": "inventory service"}



@app.post("/add-inventory/")
async def generate_inventory(inventory: InventoryItems, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    """ Create a new inventory and send it to Kafka"""
    
    inventory_dict = {field: getattr(inventory, field) for field in inventory.dict()}
    inventory_json = json.dumps(inventory_dict,cls=CustomJSONEncoder).encode("utf-8")
    
    print("inventory_JSON:", inventory_json)
    # Produce message
    await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_json)
    
    return inventory








@app.get("/all-inventory/",response_model=List[InventoryItems])
def get_all_inventory(session: Annotated[Session, Depends(get_session)]):
    """ Get all inventory items"""
    try:
        return get_all_inventories(session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @app.patch("/update-order-status")
# def update_order_status(order_id:int,order_status:OrderStatus,session: Annotated[Session, Depends(get_session)]):

#     try:
#         return order_status_update(order_id=order_id,order_status=order_status,session=session)
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
from contextlib import asynccontextmanager

from fastapi import FastAPI,Depends
from typing import Annotated 


from src.DB.db import create_db_and_tables
from src.Model.model import User,Inventory,Notification,Category,OrderItems,Orders,Product,SubCategory,Warehouse,Payments 
from src.Service.service import register_user,all_product,create_product,create_category,create_sub_category,create_order,create_order_items,pay_payment,warehouse,inventory_create

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    # delete_all_tables()
    yield



app: FastAPI = FastAPI(lifespan=lifespan)




@app.get("/")
def root()->dict:
    return {"message":"root working fine"}

@app.post("/signup")
async def create_user(user:Annotated[User,Depends(register_user)]):
    return user



@app.post("/add-product")
async def add_product(product:Annotated[Product,Depends(create_product)]):
    return product

@app.post("/add-category")
async def add_category(category:Annotated[Category,Depends(create_category)]):
    return category 

@app.post("/add-sub-category")
async def add_sub_category(sub_category:Annotated[SubCategory,Depends(create_sub_category)]):
    return sub_category

@app.post("/order")
async def add_order(order:Annotated[Orders,Depends(create_order)]):
    return order 

@app.post("/order-items")
async def order_items(order_items:Annotated[OrderItems,Depends(create_order_items)]):
    return order_items 

@app.post("/procced-payment")
async def payment_procced(payment:Annotated[Payments,Depends(pay_payment)]):
    return pay_payment 

@app.post("/warehouse")
async def warehouse_info(warehouse_detail:Annotated[Warehouse,Depends(warehouse)]):
    return warehouse_info


@app.post("/inventory")
async def create_invetory(inventory:Annotated[Inventory,Depends(inventory_create)]):
    return inventory_create


@app.get("/all-product")
async def get_products(products:Annotated[Product,Depends(all_product)]):
    return products 

from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends
from typing import Annotated 



from src.Model.e_model import User,Product,Order,Payment,Address,Cart,Category 
from src.DB.db import create_db_and_tables
from src.Service.e_service import register_user,get_user,get_user_orders,get_user_order,get_user_cart

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app: FastAPI = FastAPI(lifespan=lifespan)




@app.get("/")
def root()->dict:
    return {"message":"root working fine"}


@app.post("/add-users")
async def create_user(user_data:Annotated[User,Depends(register_user)]):
    return user_data

# @app.post("/login")
# async def create_user(user_data:Annotated[User,Depends(register_user)]):
#     return user_data

@app.get("/user/profile")
async def get_user_profile(user:Annotated[User,Depends(get_user)]):
    return user 

@app.get("/user/orders")
async def user_orders(orders:Annotated[Order,Depends(get_user_orders)]):
    return orders


@app.get("/user/order")
async def user_order(order:Annotated[Order,Depends(get_user_order)]):
    return order

@app.get('/user-cart')
async def user_cart(cart:Annotated[Cart,Depends(get_user_cart)]):
    return cart







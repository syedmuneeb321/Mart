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
from app.models.user_model import User,UserPublic,UserCreate #ProductUpdate
from app.crud.user_crud import create_user,user_login,role_assign_by_admin,CurrentUser,get_all_users,update_user
from app.deps import get_session, get_kafka_producer,DBSessionDep

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)




# The first part of the function, before the yield, will
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating table!")

    
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)



@app.get("/")
def read_root():
    return {"Hello": "user Service"}


@app.post("/register-user/", response_model=UserPublic)
async def create_new_product(user: UserCreate, session: DBSessionDep):
    """ Create a new product and send it to Kafka"""
    
    return create_user(user_data=user,session=session)
    
    

@app.post("/user-login")
def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)],session: Annotated[Session, Depends(get_session)]):
    """ Get all products from the database"""
    user = user_login(form_data=form_data,session=session)
    return user

@app.post("/role-assign/", response_model=UserPublic)
def get_single_product(user_data:UserCreate,session:DBSessionDep):
    """ Get a single product by ID"""
    try:
        return role_assign_by_admin(user_data=user_data,session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/user/me',response_model=UserPublic)
async def get_user_me(user:CurrentUser):
    return user

@app.get("/get-all-user",response_model=list[UserPublic])
def all_user(users:Annotated[UserPublic,Depends(get_all_users)]):
    return users

@app.patch("/user-update/",response_model=UserPublic)
def user_update(user: Annotated[UserPublic, Depends(update_user)]):
    """ Update a single user inforamtion like email etc."""
    try:
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# baqi functionallity bad mein kare ge user service ke related

# @app.delete("/manage-products/{product_id}", response_model=dict)
# def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    
    
#     """ Delete a single product by ID"""
#     try:
#         return delete_product_by_id(product_id=product_id, session=session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

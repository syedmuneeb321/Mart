from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated

from src.DB.db import get_session
from src.Utils.utils import get_password_hash, verify_password
from src.Model.e_model import User, Product, Order, Payment, Address, Cart, Category


async def register_user(user: User, session: Annotated[Session, Depends(get_session)]):

    user_exists_db: User = session.exec(
        select(User).where(User.username == user.username)
    ).first()

    if user_exists_db:
        raise HTTPException(status_code=400, detail="User Already Exist")

    password = get_password_hash(user.password)

    user_data = User.model_validate(user, update={"password": password})
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data





async def get_user(id:int,session: Annotated[Session, Depends(get_session)]):
    user_in_db: User = session.get(User,id)
    if not user_in_db:
        raise HTTPException(status_code=404,detail="invalid creadientls provide")
    return user_in_db

async def get_user_orders(id:int,session: Annotated[Session, Depends(get_session)]):
    user: User = session.get(User,id)
    order = user.orders
    return order

async def get_user_order(id:int,session:Annotated[Session,Depends(get_session)]):
    order = session.get(Order,id)
    if not order:
        raise HTTPException(status_code=404,detail="not found order")
    return order

async def get_user_cart(id: int, session:Annotated[Session,Depends(get_session)]):
    user = session.get(User,id)
    return user.cart

    

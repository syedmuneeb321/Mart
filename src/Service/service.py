from fastapi import Depends,HTTPException
from sqlmodel import Session,select 
from typing import Annotated

from src.Model.model import User,Product,Category,SubCategory,Orders,OrderItems,Payments,Notification,Warehouse,Inventory 
from src.DB.db import get_session


async def register_user(user:User,session:Annotated[Session,Depends(get_session)]):
    user_in_exits_db = session.exec(select(User).where(User.username == user.username)).first()
    
    if user_in_exits_db:
        raise HTTPException(status_code=400,detail="user already exists")
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 





# async def login()


async def create_product(product:Product,session:Annotated[Session,Depends(get_session)]):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


async def all_product(session:Annotated[Session,Depends(get_session)]):
    return session.exec(select(Product)).all()


async def create_category(category:Category,session:Annotated[Session,Depends(get_session)]):
    category_exist_in_db = session.exec(select(Category).where(Category.name==category.name)).first()

    if category_exist_in_db:
        return category_exist_in_db
    
    session.add(category)
    session.commit()
    session.refresh(category)
    return category 


async def create_sub_category(sub_category:SubCategory,session:Annotated[Session,Depends(get_session)]):
    sub_category_exist_in_db = session.exec(select(SubCategory).where(SubCategory.name==sub_category.name)).first()

    if sub_category_exist_in_db:
        return sub_category_exist_in_db
    
    session.add(sub_category)
    session.commit()
    session.refresh(sub_category)
    return sub_category 


async def create_order(order:Orders,session:Annotated[Session,Depends(get_session)]):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order 


async def create_order_items(order_items:OrderItems,session:Annotated[Session,Depends(get_session)]):
    session.add(order_items)
    session.commit()
    session.refresh(order_items)
    return order_items 



async def pay_payment(pay:Payments,session:Annotated[Session,Depends(get_session)]):
    session.add(pay) 
    session.commit()   
    session.refresh(pay)
    return pay 


async def create_notification(notification:Notification,session:Annotated[Session,Depends(get_session)]):
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


async def warehouse(warehouse_info:Warehouse,session:Annotated[Session,Depends(get_session)]):
    session.add(warehouse_info)
    session.commit()
    session.refresh(warehouse_info)
    return warehouse_info 

async def inventory_create(inventory:Inventory,session:Annotated[Session,Depends(get_session)]):
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory 



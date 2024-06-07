from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timedelta,timezone
from typing import List,Optional

class Address(SQLModel,table=True):
    id: int| None = Field(default=None,primary_key=True)
    address: str 
    city: str 
    country: str 
    zipcode: int 
    order_id: int = Field(foreign_key="order.id")
    orders: List["Order"] = Relationship(back_populates="address")



class orderItems(SQLModel,table=True):
    id: int| None = Field(default=None,primary_key=True)
    product_id: int 
    price: float  
    quantity: int 


class Order(SQLModel,table=True):
    id: int| None = Field(default=None,primary_key=True)
    customer_id: int 
    # orders: 
    total_price: float 
    address: Address = Relationship(back_populates="address")


    


    
    

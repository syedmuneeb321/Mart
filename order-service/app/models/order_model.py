from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timedelta,timezone
from typing import List,Optional
import enum

class OrderStatus(str,enum.Enum):
    pending = "pending"
    process = "process"
    completed = "completed"
    cancelled = "cancelled"

class PaymentStatus(str,enum.Enum):
    paid = "paid"
    unpaid = "unpaid"



class Address(SQLModel,table=True):
    id: int| None = Field(default=None,primary_key=True)
    address: str 
    city: str 
    country: str 
    zipcode: int 
    
    user_id: int 
    
    orders: List["Order"] = Relationship(back_populates="address")



# # class orderItems(SQLModel,table=True):
# #     id: int| None = Field(default=None,primary_key=True)
# #     product_id: int 
# #     price: float  
# #     quantity: int 



class Order(SQLModel,table=True):
    id: int| None = Field(default=None,primary_key=True)
    customer_id: int 
    product_id: int  
    total_price: float
    quantity: int = Field(default=1)
    address_id: int = Field(foreign_key ="address.id")
    address: Address = Relationship(back_populates="orders")

    status:OrderStatus = Field(default=OrderStatus.pending)
    payment_status: PaymentStatus = Field(default=PaymentStatus.unpaid)


    

    
    

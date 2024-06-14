from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timedelta,timezone
from typing import List,Optional
import enum


class BaseAddress(SQLModel):
    address: str 
    city: str 
    country: str 
    zipcode: int 

class Address(BaseAddress,table=True):
    id: int| None = Field(default=None,primary_key=True)
    user_id: int 
    orders: List["Order"] = Relationship(back_populates="address")

class CreateUserAddress(BaseAddress):
    pass

class UpdateAddress(SQLModel):
    address: str | None = None
    city: str | None = None
    country: str | None = None
    zipcode: int | None = None






class OrderStatus(str,enum.Enum):
    pending = "pending"
    process = "process"
    completed = "completed"
    cancelled = "cancelled"

class PaymentStatus(str,enum.Enum):
    paid = "paid"
    unpaid = "unpaid"

# # class orderItems(SQLModel,table=True):
# #     id: int| None = Field(default=None,primary_key=True)
# #     product_id: int 
# #     price: float  
# #     quantity: int 

class BaseOrder(SQLModel):
    product_id: int  
    total_price: float
    quantity: int = Field(default=1)
    address_id: int = Field(foreign_key ="address.id")

class Order(BaseOrder,table=True):
    id: int| None = Field(default=None,primary_key=True)
    customer_id: int 
    address: Address = Relationship(back_populates="orders")
    status:OrderStatus = Field(default=OrderStatus.pending)
    payment_status: PaymentStatus = Field(default=PaymentStatus.unpaid)


    
class CreateOrder(BaseOrder):
    pass 


    

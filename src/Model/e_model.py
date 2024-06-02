from sqlmodel import SQLModel,Field,Relationship
from datetime import datetime,timezone,timedelta
import enum 
from typing import List,Optional




class Role(enum.Enum):
    Admin = "Admin"
    User = "User"


class User(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    username:str 
    email:str 
    password:str 
    name:str 
    phone: str 
    role:Role = Field(default=Role.User)
    addresses: Optional[List['Address']] = Relationship(back_populates="user")
    products: Optional[List['Product']] = Relationship(back_populates='user')
    cart: Optional['Cart'] = Relationship(back_populates='user')

    orders: List["Order"] = Relationship(back_populates="customer")
    payments: List["Payment"] = Relationship(back_populates="customer")
    

class Address(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    address_1: str 
    address_2: str 
    city: str 
    country: str 
    pine_code: str 
    # state: str
    user_id : int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="addresses")
    # products: List['Product'] = Relationship(back_populates="address")
    order: "Order" = Relationship(back_populates="address")



class Category(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    name: str 
    products: List['Product'] = Relationship(back_populates="category")


class CartProductLink(SQLModel,table=True):
    product_id: int |None = Field(foreign_key='product.id',primary_key=True,default=None)
    cart_id: int | None = Field(default=None,foreign_key='cart.id',primary_key=True)
    product_quantiy: int = Field()
    product: "Product" = Relationship(back_populates="cart_link")
    cart: "Cart" = Relationship(back_populates="product_link")

class ProductOrderLink(SQLModel,table=True):
    product_id: int|None = Field(foreign_key='product.id',primary_key=True,default=None)
    order_id: int|None = Field(foreign_key='order.id',primary_key=True,default=None)
    quantity: int

    order: "Order" = Relationship(back_populates="product_link")
    product: "Product" = Relationship(back_populates="order_link")

    

class Product(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    name: str 
    description: str 
    image_url: str 
    price:float 
    stock: int 

    category_id: int = Field(foreign_key='category.id')
    category: Category = Relationship(back_populates="products")

    user_id:  int = Field(foreign_key='user.id')
    user: User = Relationship(back_populates='products')

    cart_link: List[CartProductLink] = Relationship(back_populates="product")

    order_link: List[ProductOrderLink] = Relationship(back_populates="product")






class Cart(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="cart")

    product_link: list[CartProductLink] = Relationship(back_populates="cart")

    

    







class OrderStatus(enum.Enum):
    
    Pending = "Pending"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Cancelled = "Cancelled"

class Order(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    customer_id: int = Field(foreign_key="user.id")
    customer: User = Relationship(back_populates="orders")

    product_link: List[ProductOrderLink] = Relationship(back_populates="order")

    address_id: int = Field(foreign_key='address.id')
    address: Address = Relationship(back_populates="order")

    status: OrderStatus = Field(default=OrderStatus.Pending)
    payment_id: int = Field(foreign_key='payment.id')
    payment: "Payment" = Relationship(back_populates='orders')


class Payment(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    orders: Order = Relationship(back_populates="payment")
    customer_id: int = Field(foreign_key="user.id")
    customer: User = Relationship(back_populates="payments")
    payments_method: str 
    payment_date: datetime = Field(default_factory=datetime.now)
    amount: float







    
















from sqlmodel import SQLModel,Field
from datetime import datetime,timezone,timedelta
import enum 


class Role(enum.Enum):
    Admin = "Admin"
    Customer = "Customer"
    Seller = "Seller"

class User(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    username:str 
    email:str 
    password:str 
    name:str 
    address:str
    phone: str 
    role:Role = Field(default=Role.Customer) 

class Category(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    name:str

class SubCategory(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    name:str 
    category_id: int = Field(foreign_key="category.id")




class Product(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    name:str
    description:str
    price:int 
    category: int = Field(foreign_key="category.id")
    subcategory:int = Field(foreign_key="subcategory.id")
    brand: str 
    image_url : str 
    seller_id: int = Field(foreign_key="user.id")


class OrderStatus(enum.Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Cancelled = "Cancelled"


class Orders(SQLModel,table=True):
    id:int|None = Field(default=None,primary_key=True)
    user_id: int =Field(foreign_key='user.id') 
    order_date:datetime = Field(default_factory=datetime.now)
    total_cost: float 
    status: OrderStatus = Field(default=OrderStatus.Pending)





class OrderItems(SQLModel,table=True):
    id: int|None = Field(default=None,primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id : int = Field(foreign_key="product.id")
    quantity: int 
    unit_price: float

class Payments(SQLModel,table=True):
    id: int|None = Field(default=None,primary_key=True)
    order_id: int = Field(foreign_key='orders.id')
    payments_method: str 
    payment_date: datetime = Field(default_factory=datetime.now)
    amount: float 

class Notification(SQLModel,table=True):
    id: int|None = Field(default=None,primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    order_id : int = Field(foreign_key="orders.id")
    message: str 








class Inventory(SQLModel,table=True):
    id: int|None = Field(default=None,primary_key=True)
    product_id: int = Field(foreign_key='product.id')
    warehouse_id: int = Field(foreign_key="warehouse.id")
    quantity: int 
    reorder_level: int 
    reorder_quantity: int 


class Warehouse(SQLModel,table=True):
    id: int|None = Field(default=None,primary_key=True)
    name: str 
    location: str



# This design includes the following relationships:

# - A user can make many orders (one-to-many).
# - An order is associated with one user (many-to-one).
# - An order can have many order items (one-to-many).
# - An order item is associated with one order and one product (many-to-one).
# - A product can have many order items (one-to-many).
# - A product can have many inventory entries (one-to-many).
# - An inventory entry is associated with one product and one warehouse (many-to-one).
# - A notification is associated with one user and one order (many-to-one).
# - A payment is associated with one order (many-to-one).

# Note that this is just one possible design, and you may need to modify it based on specific requirements and constraints. Additionally, you may want to consider adding indexes, constraints, and triggers to ensure data consistency and improve query performance.


 
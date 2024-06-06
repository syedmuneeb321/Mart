from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timedelta,timezone
import enum

class Role(str,enum.Enum):
    admin = "admin"
    customer = "customer"


class BaseUser(SQLModel):
    user_name: str = Field(index=True,unique=True)
    email: str = Field(index=True,unique=True)
    
    role: Role = Field(default=Role.customer)

class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str 
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now,sa_column_kwargs={"onupdate":datetime.now})

class UserCreate(BaseUser):
    password: str  

class UserPublic(BaseUser):
    # id: int 
    pass


    


    
    

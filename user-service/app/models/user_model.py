from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timedelta,timezone
import enum

class Role(str,enum.Enum):
    admin = "admin"
    customer = "customer"


class BaseUser(SQLModel):
    user_name: str = Field(index=True,unique=True)
    email: str = Field(index=True,unique=True)
    
    

class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str 
    role: Role = Field(default=Role.customer)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow,sa_column_kwargs={"onupdate":datetime.now})

class UserCreate(BaseUser):
    password: str  

class UserPublic(BaseUser):
    id: int 



class UserUpdate(SQLModel):
    user_name:str | None
    email: str | None

    


    
    

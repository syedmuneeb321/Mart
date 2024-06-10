from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime,timedelta,timezone
from typing import List,Optional
import enum
import uuid
from sqlalchemy import text



class InventoryItems(SQLModel,table=True):
    id: uuid.UUID  = Field(default_factory=uuid.uuid4,primary_key=True,nullable=False)
    product_id: int 
    quantity: int 
    

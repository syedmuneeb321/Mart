from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItems




def create_inventory_item(item: InventoryItems, session: Session):

    print("\n\n saving date to database")
    print("\n\n item in crud", item)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item



# create a get all inventory function
def get_all_inventories(session:Session):
    items = session.exec(select(InventoryItems)).all()
    return items
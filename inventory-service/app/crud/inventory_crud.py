from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItems,InvetoryItemsUpdate
from uuid import UUID




def create_inventory_item(item: InventoryItems, session: Session):

    # print("\n\n saving date to database")
    # print("\n\n item in crud", item)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item



# create a get all inventory function
def get_all_inventories(session:Session):
    items = session.exec(select(InventoryItems)).all()
    return items

def inventory_update(item_id:UUID,item:InventoryItems,session:Session):
    db_item = session.get(InventoryItems,item_id)
    item_data = item.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item 


def delete_invetory_item(item_id:UUID,session:Session):
    invetory_item = session.get(InventoryItems,item_id)
    if invetory_item is None:
        raise HTTPException(status_code=404, detail="item not found")
    session.delete(invetory_item)
    session.commit()
    return {"message": "Product Deleted Successfully"}


from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.payment_model import Payment,PaymentStatus
from uuid import UUID




def create_order_payment(payment: Payment, session: Session):
    # print("\n\n saving date to database")
    # print("\n\n payment in crud", payment)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment



# create a get all inventory function
# def get_all_inventories(session:Session):
#     items = session.exec(select(InventoryItems)).all()
#     return items

def payment_status_update(item_id:UUID,payment_status:PaymentStatus,session:Session):
    db_item: Payment | None = session.get(Payment,item_id)
    if db_item is not None:
        db_item.payment_status = payment_status
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    


# def delete_invetory_item(item_id:UUID,session:Session):
#     invetory_item = session.get(InventoryItems,item_id)
#     if invetory_item is None:
#         raise HTTPException(status_code=404, detail="item not found")
#     session.delete(invetory_item)
#     session.commit()
#     return {"message": "Product Deleted Successfully"}


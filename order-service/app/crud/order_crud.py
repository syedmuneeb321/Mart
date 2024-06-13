from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.order_model import Address,UpdateAddress,Order,OrderStatus,PaymentStatus


# Add a New order to the Database
def create_order(order_data: Order, session: Session):
    print("Adding order to Database")
    session.add(order_data)
    session.commit()
    session.refresh(order_data)
    return order_data


# Add a New address to the Database
def create_address(address_data: Address, session: Session):
    print("Adding address to Database")
    
    session.add(address_data)
    session.commit()
    session.refresh(address_data)
    return address_data


def get_address(id:int,session:Session):
    addresses = session.exec(select(Address).where(Address.user_id==id)).all()
    return addresses

def update_address(address_id:int,user_id:int,address:UpdateAddress,session:Session):
    user_db_address = session.exec(select(Address))


def get_customer_orders(customer_id: int,session:Session):
    orders = session.exec(select(Order).where(Order.customer_id==customer_id)).all()
    return orders



def order_status_update(order_id:int,order_status:OrderStatus,session:Session):
    order = session.get(Order,order_id)
    order.status = order_status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
    
def order_peyment_update(order_id:int,order_payment_status:PaymentStatus,session:Session):
    order = session.get(Order,order_id)
    order.payment_status = order_payment_status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def verify_order(order_id:int,session:Session):
    order_exist: Order = session.get(Order,order_id)
    if order_exist:
        return order_exist



# # Get All Products from the Database
# def user_login(form_data:dict,session: Session):
#     user_in_db = session.exec(select(User).where(User.user_name == form_data.username)).first()
#     if not user_in_db:
#         raise HTTPException(status_code=404,detail="invalid credentials")
#     if not verify_password(form_data.password,user_in_db.password):
#         raise HTTPException(status_code=404,detail="invalid credientials")
    
#     return user_in_db 
    
    # all_products = session.exec(select(Product)).all()
    # return all_products

# # Get a Product by ID
# def get_product_by_id(product_id: int, session: Session):
#     product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

# # Delete Product by ID
# def delete_product_by_id(product_id: int, session: Session):
#     # Step 1: Get the Product by ID
#     product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     # Step 2: Delete the Product
#     session.delete(product)
#     session.commit()
#     return {"message": "Product Deleted Successfully"}

# # Update Product by ID
# def update_product_by_id(product_id: int, to_update_product_data:ProductUpdate, session: Session):
#     # Step 1: Get the Product by ID
#     product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     # Step 2: Update the Product
#     hero_data = to_update_product_data.model_dump(exclude_unset=True)
#     product.sqlmodel_update(hero_data)
#     session.add(product)
#     session.commit()
#     return product
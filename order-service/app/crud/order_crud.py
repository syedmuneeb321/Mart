from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user_model import User,UserCreate #ProductUpdate
from app.utils.security import verify_password,get_password_hash


# Add a New Product to the Database
def create_user(user_data: UserCreate, session: Session):
    print("Adding user to Database")
    hashed_password = get_password_hash(user_data.password)
    user_data = User.model_validate(user_data,update={"password":hashed_password})
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

# # Get All Products from the Database
def user_login(form_data:dict,session: Session):
    user_in_db = session.exec(select(User).where(User.user_name == form_data.username)).first()
    if not user_in_db:
        raise HTTPException(status_code=404,detail="invalid credentials")
    if not verify_password(form_data.password,user_in_db.password):
        raise HTTPException(status_code=404,detail="invalid credientials")
    
    return user_in_db 
    
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
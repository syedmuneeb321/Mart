from typing import Annotated
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from datetime import timedelta
from jose import jwt,JWTError

from app.models.user_model import User,UserCreate,Role
from app.utils.security import verify_password,get_password_hash,create_access_token,ALGORITHM
from app.deps import DBSessionDep
from app import settings




reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="user-login"
)

TokenDep = Annotated[str,Depends(reusable_oauth2)]



def get_current_user(session:DBSessionDep , token:TokenDep):
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(f"inside ge current user payload data: {payload}")
        username = payload.get('sub')
    
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = session.exec(select(User).where(User.user_name == username)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    return user

CurrentUser = Annotated[User,Depends(get_current_user)]
# create new costomer user
def create_user(user_data: UserCreate, session: Session):
    print("Adding user to Database")
    hashed_password = get_password_hash(user_data.password)
    user_data = User.model_validate(user_data,update={"password":hashed_password})
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

# user login and accesstoken
def user_login(form_data:dict,session: Session):
    user_in_db = session.exec(select(User).where(User.user_name == form_data.username)).first()
    if not user_in_db:
        raise HTTPException(status_code=404,detail="invalid password and username")
    if not verify_password(form_data.password,user_in_db.password):
        raise HTTPException(status_code=404,detail="invalid username and password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_data = create_access_token(subject=user_in_db.user_name,expires_delta=access_token_expires)
    return {
        "access_token":token_data,
        "token_type":"bearer"
    }
    
    

# # Get a Product by ID
def role_assign_by_admin(user_data:UserCreate,session:Session):
    user_in_db = session.exec(select(User).where(User.user_name == user_data.user_name).where(User.email==user_data.email)).one_or_none()
    if not user_in_db:
        raise HTTPException(status_code=404,detail="invalid credentials")
    
    if not verify_password(user_data.password,user_in_db.password):
        raise HTTPException(status_code=404,detail="invalid credientials")

    user_in_db.role = Role.admin
    session.add(user_in_db)
    session.commit()
    session.refresh(user_in_db)
    return user_in_db
    


# get all user 
def get_all_users(session:DBSessionDep,user:CurrentUser):
    if not user.role == 'admin':
        raise HTTPException(status_code=403,detail="The user doesn't have enough privileges")
    users = session.exec(select(User)).all()

    return users


def update_user(user_data:,session:DBSessionDep)

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
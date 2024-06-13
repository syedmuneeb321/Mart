from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from aiokafka import AIOKafkaProducer
from sqlmodel import Session
from typing import Annotated, Any
from requests import get,post

from app.db_engine import engine
from app import settings
# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


GetProducerDeps = Annotated[AIOKafkaProducer,Depends(get_kafka_producer)]

def get_session():
    with Session(engine) as session:
        yield session


DbSessionDeps = Annotated[Session,Depends(get_session)]

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

# TokenDeps = Annotated[str,Depends(oauth2_scheme)]

def verify_access_token(token:Annotated[str,Depends(oauth2_scheme)]):
    headers = {"Authorization": f"Bearer {token}"}

    response = get(f"{settings.AUTH_SERVER_URL}/token-verify",headers=headers)
    # print(response)
    if response.status_code == 200:
        return response.json()
    

CurrentUserDeps = Annotated[dict,Depends(verify_access_token)]

def get_login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    data = {
        "username":form_data.username,
        "password":form_data.password
    }
    print(data)
    response = post(f"{settings.AUTH_SERVER_URL}/user-login",data=data)
    print(response)
    return response.json()


LoginForAccessTokenDeps = Annotated[dict,Depends(get_login_for_access_token)]

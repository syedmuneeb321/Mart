from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from aiokafka import AIOKafkaProducer
from sqlmodel import Session
from typing import Annotated
from requests import post,get 

from app.db_engine import engine
from app import settings

oauth_2scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

ProducerDeps = Annotated[AIOKafkaProducer,Depends(get_kafka_producer)]

def get_session():
    with Session(engine) as session:
        yield session

DbSessionDeps = Annotated[Session,Depends(get_session)]




def auth_token_verify(token:Annotated[str,Depends(oauth_2scheme)]):
    headers = {
        "Authorization":f"Bearer {token}"
    }

    response = get(f"{settings.AUTH_SERVER_URL}/token-verify",headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json()['role'] == "admin"
    
    raise HTTPException(status_code=401, detail="Unauthorized")



TokenDeps = Annotated[bool,Depends(auth_token_verify)]





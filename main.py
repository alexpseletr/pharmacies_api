import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer, APIKeyHeader
from pydantic import BaseModel
from typing import List
import databases
import sqlalchemy
from datetime import datetime

API_KEY = "chave_de_api_fixa"
AUTH_TOKEN = "token_de_autorizacao_fixo"

DATABASE_URL = "sqlite:///./backend_test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

class PatientResponse(BaseModel):
    uuid:str
    first_name: str
    last_name: str
    date_of_birth: datetime

class PharmacyResponse(BaseModel):
    uuid: str
    name: str
    city: str

class TransactionResponse(BaseModel):
    patient_uuid: str
    patient_name: str
    patient_lastname: str
    patient_birty: datetime
    pharmacy_uuid: str
    pharmacy_name: str
    pharmacy_city: str
    uuid: str
    amount: float
    timestamp: datetime

class TokenData(BaseModel):
    username: str | None = None

patients = sqlalchemy.Table(
    "patients",
    metadata,
    sqlalchemy.Column("uuid", sqlalchemy.String, primary_key=True, index=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("date_of_birth", sqlalchemy.Date),
)

pharmacies = sqlalchemy.Table(
    "pharmacies",
    metadata,
    sqlalchemy.Column("uuid", sqlalchemy.String, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
)

transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    sqlalchemy.Column("patient_uuid", sqlalchemy.String),
    sqlalchemy.Column("pharmacy_uuid", sqlalchemy.String),
    sqlalchemy.Column("uuid", sqlalchemy.String, primary_key=True, index=True),
    sqlalchemy.Column("amount", sqlalchemy.Integer),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(bind=engine)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl="login",
    scopes={"read": "Read access", "write": "Write access"},
)

api_key_scheme = APIKeyHeader(name="Api-Key", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != AUTH_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token de autorização inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

def get_api_key(api_key: str = Depends(api_key_scheme)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Chave de API inválida",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/patients", response_model=List[PatientResponse])
async def list_patients(
    uuid: str = None,
    first_name: str = None,
    last_name: str = None,
    date_of_birth: datetime = None,
    api_key: str = Depends(api_key_scheme),
    current_user: TokenData = Depends(oauth2_scheme),
):
    filters = []
    if first_name:
        filters.append(patients.c.first_name == first_name)
    if last_name:
        filters.append(patients.c.last_name == last_name)
    if date_of_birth:
        filters.append(patients.c.date_of_birth == date_of_birth)

    query = patients.select()
    for f in filters:
        query = query.where(f)

    result = await database.fetch_all(query)
    return result

@app.get("/pharmacies", response_model=List[PharmacyResponse])
async def list_pharmacies(
    uuid: str = None,
    name: str = None,
    city: str = None,
    api_key: str = Depends(api_key_scheme),
    current_user: TokenData = Depends(oauth2_scheme),
):
    filters = []
    if name:
        filters.append(pharmacies.c.name == name)
    if city:
        filters.append(pharmacies.c.city == city)

    query = pharmacies.select()
    for f in filters:
        query = query.where(f)

    result = await database.fetch_all(query)
    return result

@app.get("/transactions", response_model=List[TransactionResponse])
async def list_transactions(
    patient_uuid: str = None,
    pharmacy_uuid: str = None,
    api_key: str = Depends(api_key_scheme),
    current_user: TokenData = Depends(oauth2_scheme),
):
    query = (
        transactions.join(patients, transactions.c.patient_uuid == patients.c.uuid)
        .join(pharmacies, transactions.c.pharmacy_uuid == pharmacies.c.uuid)
        .select()
    )

    if patient_uuid:
        query = query.where(transactions.c.patient_uuid == patient_uuid)
    if pharmacy_uuid:
        query = query.where(transactions.c.pharmacy_uuid == pharmacy_uuid)

    result = await database.fetch_all(query)

    transactions_response = []
    for row in result:
        transaction_data = {
            "patient_uuid": row[patients.c.uuid],
            "patient_name": row[patients.c.first_name],
            "patient_lastname": row[patients.c.last_name],
            "patient_birty": row[patients.c.date_of_birth],
            "pharmacy_uuid": row[pharmacies.c.uuid],
            "pharmacy_name": row[pharmacies.c.name],
            "pharmacy_city": row[pharmacies.c.city],
            "uuid": row[transactions.c.uuid],
            "amount": row[transactions.c.amount],
            "timestamp": row[transactions.c.timestamp],
        }
        transactions_response.append(TransactionResponse(**transaction_data))

    return transactions_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

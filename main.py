from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

def nurse_to_json(nurse):
    nurse['id'] = str(nurse['_id'])
    del nurse['_id']
    return nurse

load_dotenv()
app = FastAPI()

client = MongoClient(os.getenv("MONGODB_URI"), tlsAllowInvalidCertificates=True)


db = client.nurse_db
class InsulinChart(BaseModel):
    bg_level: str
    columns: list[float]


class NurseBase(BaseModel):
    nurse_name: str
    nurseID: str
    email: str
    password: str

class NurseLogin(BaseModel):
    nurseID: str
    password: str

@app.post("/signup/")
async def create_nurse(nurse: NurseBase):
    if db.nurses.find_one({"nurseID": nurse.nurseID}):
        raise HTTPException(status_code=400, detail="NurseID already registered")
    db.nurses.insert_one(nurse.dict())
    nurse_data1 = db.nurses.find_one({"nurseID": nurse.nurseID})
    return {"message": "Nurse created successfully"}


@app.post("/login/")
async def login_nurse(nurse: NurseLogin):
    nurse_data = db.nurses.find_one({"nurseID": nurse.nurseID, "password": nurse.password})
    if nurse_data:
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

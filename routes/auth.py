from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from passlib.context import CryptContext 

from typing import Optional

from config.config import get_mongo_db_user

# Database Connection
auth_router = APIRouter()
collection = get_mongo_db_user()
if collection is not None:
    print("Mongo Successfully Connected in auth:")
else:
    print("Mongo is not Connected")


# Pydantic Models
class User(BaseModel):
    firstName: Optional[str] = None
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

# Password Hashing Context
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hash_password(password: str) -> str:
    return pwd_context.hash(password) 

def verify_password(plain_pwd: str, hash_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hash_pwd)

@auth_router.post("/register")
async def register(user: User):
    try:
        if collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = get_hash_password(user.password)
        user_data = {
            "email": user.email,
            "password": hashed_password,
            "firstName": user.firstName
        }
        collection.insert_one(user_data)

        return {
            "status": "success",
            "data": {"email": user.email, "firstName": user.firstName}
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": None
        }

@auth_router.post("/login")
async def login(user: LoginUser):
    try:
        # Check if user exists
        db_user = collection.find_one({"email": user.email})
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid email or password")


        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        return {
            "status": "success",
            "message": "Login successful",
            "data": {"email": db_user["email"], "firstName": db_user.get("firstName", "")}
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": None
        }

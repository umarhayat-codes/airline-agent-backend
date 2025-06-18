from fastapi import APIRouter
from pydantic import BaseModel

from config.config import get_mongo_collection 


collection = get_mongo_collection()
if collection is not None:
    print("Mongo Successfully Connection")
else:
    print("Connection Failed")


product_router = APIRouter()
class Product(BaseModel):
    name : str
    price : float
    description : str



@product_router.post("/create")
async def create_product(product:Product):
    try:
        collection.insert_one(product.dict())
        return {
            "status":"Successfully create",
            "data": product
        }
    except Exception as e:
        
        return {
            "message":str(e),
            "status":"error",
            "data":None
        }
    

@product_router.get("/get")
async def get_product():
    try:
        products = list(collection.find())
        for product in products:
            product['_id'] = str(product['_id'])
        return {
            "status":"success",
            "data": products
        }
    except Exception as e:
        return {
            "message":str(e),
            "status":"error",
            "data":None
        }


@product_router.delete("/delete")
async def deleteProduct():
    pass

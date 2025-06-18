from fastapi import APIRouter
from pydantic import BaseModel

from config.config import get_mongo_collection


collection = get_mongo_collection()
if collection is not None:
    print("Mongo Successfully Connection")
else:
    print("Connection Failed")


database_router = APIRouter()

class AirLine(BaseModel):
    answer:str



@database_router.post("/create")
async def create_product(answer:AirLine):
    try:
        collection.insert_one(answer.dict())
        return {
            "status":"Successfully create",
            "data": answer
        }
    except Exception as e:
        
        return {
            "message":str(e),
            "status":"error",
            "data":None
        }
    

# @product_router.get("/get")
# async def get_product():
#     try:
#         products = list(collection.find())
#         for product in products:
#             product['_id'] = str(product['_id'])
#         return {
#             "status":"success",
#             "data": products
#         }
#     except Exception as e:
#         return {
#             "message":str(e),
#             "status":"error",
#             "data":None
#         }


# @product_router.delete("/delete")
# async def deleteProduct():
#     pass

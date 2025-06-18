from fastapi import FastAPI

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from config import get_mongo_collection

collection = get_mongo_collection()
if collection is not None:
    print("Mongo Connect Successfully:")
else:
    print("Failed Connection")

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Product(BaseModel):
    name : str
    price : float
    description : str

@app.post("/create/product")
async def create_product(product : Product):
    a = await collection.insert_one(product)
    print(a)
    try:
        # await collection.insert_one(product)
        return {
            "status":"success",
            "data":product,
            "message":"Product Successfully Created"
        }
    except Exception as e:
        print({
            "message":str(e),
            "status":"error",
            "data":None
        })
        return {
            "status":"error",
            "message":str(e),
            "data":None
        }
    
@app.get("/get/product")
async def get_product():
    try:
        products = await list(collection.find())
        for product in products:
            product["_id"] = str(product['_id'])
        return {
            "status":"success",
            "data":products
        }
    except Exception as e:
        return {
            "status":"error",
            "data":None,
            "message":str(e)
        }
    



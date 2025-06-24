from fastapi import FastAPI


from fastapi.middleware.cors import CORSMiddleware

from routes.gmail_send_route import gmail_send_router

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(gmail_send_router,prefix='/gmail-send')

# from pydantic import BaseModel


# class User(BaseModel):
#     name : str
#     age : int
#     description : str

# u_1 = {"name" : "hi","age":12,"description":"Male"}
# user = User(**u_1)
# print(user)



# from fastapi import FastAPI
# from pydantic import BaseModel
# app = FastAPI()

# class Product(BaseModel):
#     name : str
#     price : int
#     description : str

# @app.post('/create/product')
# async def create_product(product : Product):
#     return {"message":"Successfully Create","product":product}

# product = Product(name = "umar",price=2,description="Product")
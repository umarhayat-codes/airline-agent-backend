from fastapi import FastAPI

# from routes.auth import auth_router
# from routes.product import product_router
from routes.air_line_route import air_agent_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#  "fastapi[standard] (>=0.115.6,<0.116.0)",
#     "uvicorn (>=0.34.0,<0.35.0)",
#     "pymongo (>=4.10.1,<5.0.0)",
#     "python-dotenv (>=1.0.1,<2.0.0)",
#     "passlib (>=1.7.4,<2.0.0)",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(air_agent_router,prefix='/air-agent')
# app.include_router(auth_router,prefix='/auth')
# app.include_router(product_router,prefix='/product')
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
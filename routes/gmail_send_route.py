from fastapi import APIRouter
from pydantic import BaseModel
# import asyncio

from tools.gmail_send_tool import gmail_send_agent
from agents import Runner

gmail_send_router = APIRouter()

class EmailQuery(BaseModel):
    query: str  # e.g. "Send an email about internship update to example@gmail.com from my Gmail"

@gmail_send_router.post("/")
async def run_email_agent(query: EmailQuery):
    try:
        print("query from frontend",query)
        result = await Runner.run(gmail_send_agent, query.query)
        # print("====================")
        # print("result : ",result)
        return {
            "result": result.final_output,
            "status":"success"
        }
    except Exception as e:
        print("error: ",str(e))
        return {
            "data":[],
            "status":"error",
            "msg":str(e)
        }
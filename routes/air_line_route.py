import json
from fastapi import APIRouter
from agents import Runner
from pydantic import BaseModel
from tools.air_line_agent_tool import agent
# from config.config import get_mongo_collection

air_agent_router = APIRouter()

class Query(BaseModel):
    query: str

# collection = get_mongo_collection()
# if collection:
#     print("Mongo Successfully Connected")
# else:
#     print("Connection Failed")


@air_agent_router.post("/airline")
async def process_airline_query(query: Query):
    try:
        print("query in backend:", query.query)

        if not query.query:
            return {"error": "Query is required"}

        # Run the agent
        result = await Runner.run(agent, query.query)

        # Safely convert output
        # data = result.final_output.dict() if hasattr(result.final_output, 'dict') else result.final_output

        # Insert into MongoDB
        # collection.insert_one({"query": query.query, "result": data})

        print("Result =>", result)



        return {
            "answer": result.final_output,
            "status": "success"
        }

    except Exception as e:
        print("Error processing query:", str(e))
        return {
            "status": "error",
            "error": str(e)
        }

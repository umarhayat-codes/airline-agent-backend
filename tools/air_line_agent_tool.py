from typing import Dict, Optional
from fastapi.background import P
from httpx import AsyncClient
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool

from dotenv import load_dotenv
from os import getenv
import asyncio

from pydantic import BaseModel

load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')
amadeus_client_id = getenv("AMADEUS_CLIENT_ID")
amadeus_client_secret = getenv("AMADEUS_CLIENT_SECRET")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)
print(gemini_api_key)
print(amadeus_client_id)
print(amadeus_client_secret)

# class FlightInfo(BaseModel):
#     airline_name: Optional[str] = None 
#     flight_number: Optional[str] = None 
#     departure_time: Optional[str] = None 
#     arrival_time: Optional[str] = None 
#     duration: Optional[str] = None 
#     economy_price: Optional[str] = None 
#     cheapest_price: Optional[str] = None 
#     seat_availability: Optional[str] = None 
#     stay_location: Optional[str] = None 




async def get_amadeus_access_token() -> str:
    async with AsyncClient() as client:
        try:
            response = await client.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": amadeus_client_id,
                    "client_secret": amadeus_client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            print("Amadeus access token response:", response)
            response.raise_for_status()
            data = response.json()
            return data["access_token"]
        except Exception as e:
            print("Failed to get Amadeus access token:", e)
            raise

if __name__ == "__main__":
    token = asyncio.run(get_amadeus_access_token())
    print("call get amadeus access token:", token)

# ✅ Flight search tool
@function_tool
async def search_flights(origin: str, destination: str, departure_date: str) -> Dict:
    
    """

    Search for flight offers using the Amadeus API.

    Args:
        origin (str): Origin airport IATA code (e.g., 'LHE').
        destination (str): Destination airport IATA code (e.g., 'DXB').
        departure_date (str): Travel date in 'YYYY-MM-DD' format.

    Returns:
        Give a answer that contain following thing :
        {
            "airline_name": "Emirates",
            "flight_number": "EK611",
            "departure_time": "2025-06-16T09:30:00",
            "arrival_time": "2025-06-16T12:45:00",
            "duration": "3h 15m",
            "economy_price": "250 USD",
            "cheapest_price": "220 USD",
            "seat_availability": "Available",
            "stay_location": "Dubai"
        }

    """


    token = await get_amadeus_access_token()
    
    async with AsyncClient() as Client:
        response = await Client.get(
            "https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure_date,
                "adults": 1,
                "children": 1,
                "currencyCode": "USD",
                "max": 3
            }
        )
        response.raise_for_status()
        print("===================")
        print("res in air_line_tool =>",response.json())
        return response.json()



agent = Agent(
    name="Air line Travel Assistant",
    instructions="""
    You are a smart travel assistant. 
    When users ask for flights between cities or airports on specific dates,
    use the `search_flights` tool to retrieve the results.

    Always ask for:
    - Origin and destination in IATA format (e.g., ISB, KHI)
    - Departure date (YYYY-MM-DD)

    If the user does not provide enough information, ask follow-up questions.
    """,
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash", openai_client=client),
    tools=[search_flights],
    # output_type=FlightInfo
)

# query = input("Enter the question: ")


# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)


# result = loop.run_until_complete(
#     Runner.run(agent, query)
# )

# print(result.final_output)
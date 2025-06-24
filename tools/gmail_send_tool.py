from typing import Dict, Optional
from httpx import AsyncClient
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool

from dotenv import load_dotenv
from os import getenv
import asyncio

from pydantic import BaseModel


import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import pickle



load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)



@function_tool
async def generate_and_send_email(sender: str, receiver: str, topic: str) -> Dict:
    """
    Sends an email using the Gmail API by generating a subject and body from a given topic.

    This function is part of a Gmail Assistant Agent designed to automate the email-sending process.
    The agent performs the following steps:
    1. Asks for the sender's and receiver's Gmail addresses.
    2. Asks for a topic from which it generates a relevant email subject and body using AI.
    3. Automatically sends the generated email to the specified receiver using the Gmail API.

    Args:
        sender (str): The sender's Gmail address.
        receiver (str): The recipient's Gmail address.
        topic (str): The topic or context of the email.

    Returns:
        Dict: A dictionary containing the status of the email operation,
            the generated subject, and the message ID from the Gmail API.
    """

    try:
        # Generate subject
        subject_response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": f"Write a professional email subject about: {topic}"}],
        )
        subject = subject_response.choices[0].message.content.strip()
        print("subject: ",subject)
        # Generate body
        body_response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": f"Write a formal email body about: {topic}"}],
        )
        body = body_response.choices[0].message.content.strip()
        print("body: ",body)
        # Load Gmail credentials
        with open("token.pkl", "rb") as token_file:
            creds = pickle.load(token_file)

        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = receiver
        message['from'] = sender
        message['subject'] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        result = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        return {
            "status": "success",
            "message": "Email sent successfully.",
            "message_id": result["id"],
            "subject": subject,
            "body": body,
            "to": receiver,
            "from": sender,
            "topic": topic,
        }

    except Exception as e:
        return {"status": "error", "details": str(e)}




gmail_send_agent = Agent(
    name = "Email Assistant Agent",
    instructions = """
    You are an intelligent email assistant that helps users send emails.

    Your tasks:
    1. Ask the user for the following:
    - Sender's email address
    - Receiver's email address
    - Topic of the email

    2. Use the `generate_subject` function to create a subject based on the topic.
    3. Use the `send_email` function to compose and send the email.

    After sending the email:
    - Return a summary including the generated subject, body, sender, receiver, and confirmation (e.g., message ID).
    - Also return the full email content in your final response.
    """,
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash", openai_client=client),
    tools=[generate_and_send_email]
)


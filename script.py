# import os
# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # Step 1: Define SCOPES for Gmail
# SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# # Step 2: OAuth flow to get token
# flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
# creds = flow.run_local_server(port=0)

# # Step 3: Save the token
# with open('token.pkl', 'wb') as token:
#     pickle.dump(creds, token)

# print("✅ Authentication complete. Token saved.")


import os
import json
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

# Load .env variables
load_dotenv()

# Build credentials dictionary from environment
credentials = {
    "installed": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
    }
}

# Use the in-memory config for OAuth flow
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
flow = Flow.from_client_config(credentials, SCOPES)
creds = flow.run_local_server(port=0)

# Save the token for reuse
with open('token.pkl', 'wb') as token:
    pickle.dump(creds, token)

print("✅ Authentication complete. Token saved.")

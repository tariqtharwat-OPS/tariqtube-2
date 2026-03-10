#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Add the lite_stories_next directory to the path
sys.path.append(str(Path(__file__).parent / "lite_stories_next"))

# Scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
]

CREDENTIALS_FILE = Path("D:/TariqTube/tariqtube_next/posting/client_secret.json")
TOKEN_FILE = Path("D:/TariqTube/lite_stories_next/posting/token.pickle")

def main():
    if len(sys.argv) < 2:
        print("Usage: python finalize_auth.py <code> <state>")
        return

    code = sys.argv[1]
    state = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Finalizing auth with code: {code[:10]}...", flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), 
        SCOPES,
        state=state
    )
    
    # We must use the SAME redirect URI that was used to generate the code
    # The user's URL showed localhost:8080
    flow.redirect_uri = "http://localhost:8080/"

    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        print("✅ Token fetched successfully!", flush=True)
        
        # Save token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)
        print(f"💾 Token saved to {TOKEN_FILE}", flush=True)
        
        # Verify with YouTube
        youtube = build('youtube', 'v3', credentials=credentials)
        request = youtube.channels().list(part="snippet", mine=True)
        response = request.execute()
        
        if 'items' in response and response['items']:
            print(f"📺 Channel: {response['items'][0]['snippet']['title']}", flush=True)
        else:
            print("⚠️ No channel found.", flush=True)
            
    except Exception as e:
        print(f"❌ Failed to fetch token: {e}", flush=True)

if __name__ == "__main__":
    main()

import os
import requests
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from typing import Optional
from urllib.parse import urlencode


load_dotenv()

router = APIRouter()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')

access_token: Optional[str] = None

@router.get('/login')
def login() -> RedirectResponse:
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'r_liteprofile r_emailaddress',
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url)

@router.get('/callback')
def callback(request: Request) -> dict:
    global access_token
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()
    access_token = response_data.get('access_token')
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found in response")

    return {"access_token": access_token}

def get_access_token() -> str:
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not available")
    return access_token

import requests
from fastapi import APIRouter, Depends
from auth import get_access_token


router = APIRouter()

PROFILE_URL = 'https://api.linkedin.com/v2/me'

def get_headers(access_token: str) -> dict:
    return {
        'Authorization': f'Bearer {access_token}'
    }

@router.get('/profile')
def get_profile(access_token: str = Depends(get_access_token)) -> dict:
    headers = get_headers(access_token)
    response = requests.get(PROFILE_URL, headers=headers)
    return response.json()

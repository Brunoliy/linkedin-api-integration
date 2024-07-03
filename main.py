from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens, ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],   # Permitir todos os métodos HTTP
    allow_headers=["*"],   # Permitir todos os headers HTTP
)



@app.get("/")
def read_root():
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state=123456"
        f"&scope=r_liteprofile%20r_emailaddress"
    )
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(code: str, state: str):
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Invalid token response")

    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    email_response = requests.get(
        "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
        headers=headers
    )

    profile_json = profile_response.json()
    email_json = email_response.json()

    return {
        "profile": profile_json,
        "email": email_json
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

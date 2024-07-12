from fastapi import FastAPI
from auth import router as auth_router
from linkedin import router as linkedin_router


app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(linkedin_router, prefix="/linkedin")

@app.get('/')
def read_root() -> dict:
    return {"message": "Welcome to LinkedIn API Integration with FastAPI"}

from fastapi import FastAPI
from .auth import auth_user
from .models import User


app = FastAPI()


WIFI_LIST = {}


@app.get("/")
async def index() -> dict:
    return {
        "message": "Welcome to Auth EJUSTIAN API"
    }


@app.post("/")
async def wifi(user: User):
    req_user = auth_user(user.uid, user.pwd)
    if req_user["auth"]:
        return {
            "auth": True,
            "name": req_user["name"],
            "wifi_list": WIFI_LIST
        }
    else:
        return {"auth": False}

from fastapi import FastAPI, HTTPException
from typing import Dict
from pydantic import Base64Str
from src.service import users_service, token_services, twitt_services
from src.database.models import User, AuthUser, Twitt
from fastapi.middleware.cors import CORSMiddleware
from src.database.my_connector import Database

db = Database()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    connected = await db.connect()
    if not connected:
        raise RuntimeError("Не удалось подключиться к базе данных")


@app.get("/")
async def read_root():
    return {"Test": "Normaly Work"}


@app.get("/users/userid/{userid}", response_model=User)
async def get_user(userid: int):
    user = await users_service.get_user_by_id(userid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/username/{username}", response_model=User)
async def get_user_by_username(username: str):
    user = await users_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/email/{email}", response_model=User)
async def get_user_by_email(email: str):
    user = await users_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/register/", response_model=Dict)
async def register_user(user: User):
    try:
        user = await users_service.create_user(user)
        return {"message": "Register successful", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login/", response_model=Dict)
async def login_user(authuser: AuthUser):
    token = await token_services.authenticate_user(authuser)
    user = await users_service.get_user_by_email(authuser.email)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "token": token, "userid": user.id, "username": user.username}


@app.post("/wall/{token}", response_model=Dict)
async def get_wall_data(token: str):
    userid = await token_services.verify_token(token)
    if not userid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "Welcome to the wall", "userid": userid}


@app.post("/wall/twitt/", response_model=Dict)
async def post_twitt(twitt: Twitt):
    twittid = await twitt_services.addtwitt(twitt)
    return {"message": "Twitt add successful", "twittid": twittid}


@app.post("/wall/twitts/{limit}", response_model=list[Twitt])
async def gettwitts(limit: int):
    twitts = await twitt_services.gettwitts(limit)
    return twitts


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

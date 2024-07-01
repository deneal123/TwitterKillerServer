from src.repository import users_repository
from src.components.password import check_password
from src.components.token import generate_token
from src.database.models import User, AuthUser, Twitt
from datetime import datetime


async def get_user_by_id(userid: int):
    user = await users_repository.get_user_by_id(userid)
    return User(**user) if user else None


async def get_user_by_username(username: str):
    user = await users_repository.get_user_by_username(username)
    return User(**user) if user else None


async def get_user_by_email(email: str):
    user = await users_repository.get_user_by_email(email)
    return User(**user) if user else None


async def create_user(user: User):
    existing_user_by_email = await users_repository.get_user_by_email(user.email)
    existing_user_by_username = await users_repository.get_user_by_username(user.username)
    if existing_user_by_email or existing_user_by_username:
        raise ValueError("User already exists, check username or email")
    userid = await users_repository.create_user(user)
    return await get_user_by_id(userid)



from src.repository import token_repository
from src.service.users_service import get_user_by_email
from src.components.password import check_password
from src.components.token import generate_token
from src.database.models import AuthUser
from datetime import datetime


async def authenticate_user(authuser: AuthUser):
    user = await get_user_by_email(authuser.email)
    if user and check_password(authuser.password, user.password):
        token = generate_token(user.id)
        await token_repository.store_token(user.id, token)
        return token
    else:
        raise ValueError("User not exist or password not correct")


async def verify_token(token: str):
    data = await token_repository.verify_token(token)
    if datetime.now() < data['tokenexpiry']:
        return data['userid']

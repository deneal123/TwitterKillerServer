import aiomysql
from src.database.my_connector import Database
from src.database.models import User, Twitt
from src.components.password import hash_password, check_password
from src.components.base64decode import fix_base64_padding
db = Database()


async def get_user_by_id(userid: int):
    query = "SELECT * FROM Users WHERE id=%s"
    result = await db.fetch_one(query, (userid,))
    return result


async def get_user_by_username(username: str):
    query = "SELECT * FROM Users WHERE username=%s"
    result = await db.fetch_one(query, (username,))
    return result


async def get_user_by_email(email: str):
    query = "SELECT * FROM Users WHERE email=%s"
    result = await db.fetch_one(query, (email,))
    return result


async def create_user(user: User):
    query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
    hashed_password = hash_password(user.password)
    await db.execute_query(query, (user.username, user.email, hashed_password))
    query = "SELECT LAST_INSERT_ID()"
    result = await db.fetch_one(query)
    return result['LAST_INSERT_ID()']

import aiomysql
from src.database.my_connector import Database
from src.components.token import generate_token
from datetime import datetime, timedelta
db = Database()


async def store_token(userid: int, token: str):
    expiry = datetime.now() + timedelta(days=1)
    query = """INSERT INTO UserAuthentications (userid, token, tokenexpiry)
               VALUES (%s, %s, %s)
               ON DUPLICATE KEY UPDATE token=%s, tokenexpiry=%s"""
    await db.execute_query(query, (userid, token, expiry, token, expiry))


async def verify_token(token: str):
    query = "SELECT userid, tokenexpiry FROM UserAuthentications WHERE token = %s"
    result = await db.fetch_one(query, (token,))
    return result

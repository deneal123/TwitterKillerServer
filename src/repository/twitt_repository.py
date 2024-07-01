import aiomysql
from src.database.my_connector import Database
from src.database.models import User, Twitt
from src.components.password import hash_password, check_password
from src.components.base64decode import fix_base64_padding
import base64
import binascii
db = Database()


async def addtwitt(twitt: Twitt):
    query = "INSERT INTO Twitts (userid, text, picture) VALUES (%s, %s, %s)"
    await db.execute_query(query, (twitt.userid, twitt.text, twitt.picture))
    query = "SELECT LAST_INSERT_ID()"
    result = await db.fetch_one(query)
    return result['LAST_INSERT_ID()']


async def gettwitts(limit: int):
    query = f"SELECT * FROM Twitts ORDER BY CreatedAt DESC LIMIT {limit}"
    result = await db.fetch_all(query)
    twitts = []
    for row in result:
        twitt = {
            "ID": row["ID"],
            "UserID": row["UserID"],
            "Text": row["Text"] if row["Text"] else None,
            "Picture": None,
            "CreatedAt": row["CreatedAt"]
        }
        if row["Picture"]:
            try:
                twitt["Picture"] = base64.urlsafe_b64decode(row["Picture"])
            except binascii.Error as e:
                print(f"Ошибка декодирования base64 для строки {row['ID']}: {e}")
                twitt["Picture"] = None
        twitts.append(twitt)
    twitts.sort(key=lambda x: x["CreatedAt"])

    return twitts

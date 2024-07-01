import aiomysql
from pymysql.err import OperationalError
from datetime import datetime, timedelta
import asyncio
from src.database.models import User


class Database:
    def __init__(self):
        self.connection = None

    async def connect(self):
        try:
            self.connection = await aiomysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                db='twitterkiller',
                charset='utf8mb4',
                cursorclass=aiomysql.cursors.DictCursor
            )
            print("Подключение к базе данных успешно установлено.")
            return True
        except OperationalError as e:
            print(f"Ошибка подключения: {e}")
        return False

    async def check_and_reconnect(self):
        try:
            if self.connection is None:
                print("Подключение отсутствует или закрыто. Переподключаемся...")
                connected = await self.connect()
                if not connected:
                    print("Не удалось установить подключение.")
            else:
                await self.connection.ping()
        except OperationalError as e:
            print(f"Ошибка при проверке подключения: {e}")
            await self.connect()

    async def execute_query(self, query, params=None):
        await self.check_and_reconnect()
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, params)
            await self.connection.commit()
            return cursor

    async def fetch_one(self, query, params=None):
        await self.check_and_reconnect()
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()

    async def fetch_all(self, query, params=None):
        await self.check_and_reconnect()
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

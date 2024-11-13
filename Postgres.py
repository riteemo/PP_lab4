import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()


class Postgres:
    def __init__(self):
        self.__connection = None

    async def connect(self):
        self.__connection = await asyncpg.connect(os.getenv("DB_ADDRESS"))

    async def insert(self, username: str, artist_name: str):
        done = False
        try:
            res = await self.get_favorite_artist_by_user(username)
            if not res:
                await self.__connection.execute("INSERT INTO users (username, favorite_artist) VALUES ($1, $2)", username, artist_name)
            else:
                await self.__connection.execute("UPDATE users SET favorite_artist = $1 WHERE username = $2", artist_name, username)
            done = True
        except Exception as E:
            print(E)
        finally:
            return done

    async def get_favorite_artist_by_user(self, username: str):
        try:
            res = await self.__connection.fetch("SELECT username, favorite_artist FROM users WHERE username = $1", username)
            return res[0]['favorite_artist']
        except Exception as E:
            print(E)
            return False
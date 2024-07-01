from src.repository import twitt_repository
from src.database.models import Twitt


async def addtwitt(twitt: Twitt):
    twittid = await twitt_repository.addtwitt(twitt)
    return twittid


async def gettwitts(limit: int):
    twitts = await twitt_repository.gettwitts(limit)
    return twitts

import asyncio
from .parser import reviewParser
from .supported_markets import Market
from typing import List, Any


async def parseWebsite(link : str, market : Market) -> Any:
    result = await asyncio.to_thread(reviewParser, link, market)
    return result


async def parseMarket(links: List[str], market : Market):
    tasks = [parseWebsite(link, market) for link in links]
    results = await asyncio.gather(*tasks)
    return tuple(zip(links, results))
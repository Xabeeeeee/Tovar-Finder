import asyncio
from .parser import reviewParser, catalogParser
from .enums import Market
from typing import List, Any


async def parseReviews_single(link : str, market : Market) -> Any:
    result = await asyncio.to_thread(reviewParser, link, market)
    return result


async def parseItems_single(link : str, market : Market) -> Any:
    result = await asyncio.to_thread(catalogParser, link, market)
    return result


async def parseReviews(links: List[str], market : Market):
    tasks = [parseReviews_single(link, market) for link in links]
    results = await asyncio.gather(*tasks)
    return tuple(zip(links, results))


async def parseItems(items: List[str], market : Market):
    tasks = [parseItems_single(market.value[7].replace("{}", item), market) for item in items]
    results = await asyncio.gather(*tasks)
    return tuple(zip(items, results))
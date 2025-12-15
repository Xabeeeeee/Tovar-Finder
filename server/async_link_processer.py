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


async def parseReviews(itemlinks: List[tuple], market: Market):
    tasks = [parseReviews_single(link[1][:link[1].rfind('/')] + "/feedbacks", market) for link in itemlinks]
    results = await asyncio.gather(*tasks)
    return results


async def parseItems(items: List[dict], market : Market):
    tasks = [parseItems_single(market.value[7].replace("{}", item["model"]), market) for item in items]
    results = await asyncio.gather(*tasks)
    return results
import asyncio
from server.agent1 import *
from server.agent2 import *
from server.agent3 import *
from server.async_link_processer import parseItems
from server.async_link_processer import parseReviews

def start():
    printf("Welcome to Tovar-Finder!", color=Colors.HEADER)
    idle()


def idle():
    print_commands(["-f <description>", "-q", "-h"], ["find some item", "quit", "help"])

    command = input().strip()
    while command != "-q":
        try:
            while "  " in command: command = command.replace("  ", " ")
            match command[:2]:
                case "-f":
                    asyncio.run(processRequest(command))
                case "-h":
                    print_help_message()
                case _:
                    raise ValueError("invalid input")
        except ConnectionError:
            printf("No connection. Please try again later.", Colors.ERROR)

        print_commands(["-f <description>", "-q"], ["find some item", "quit"])
        command = input().strip()
    print("Thanks for using, see you next time!")

# -f Найди чайник 2кВт от 1000 до 5000 рублей


def print_commands(commands: list[str], descriptions: list[str]):
    print("commands:")
    offset = max(map(len, commands))
    for com, descr in zip(commands, descriptions):
        printf(com, end=('\t' * ((offset - len(com) + 3) // 4 + 1)), color=Colors.COMMAND)
        printf(descr)


def printf(message: str, color: Colors = Colors.TEXT, end='\n'):
    print(color.value + message + Colors.ENDL.value, end=end)


def print_help_message():
    printf("MANUAL:\nto search type -f and provide some description (e. g. \"-f find a powerful hair dryer "
           "between 20 and 50 bucks\")\n\nto exit program type -q", color=Colors.TEXT)


def print_tovars(tovars: list[dict], ranks: list[list[int]]):
    i = 1
    for j1, item in enumerate(tovars):
        offset = " " * 2
        printf(f"{i}.", end="")
        printf(offset + "model: ", color=Colors.BRIGHT_GREEN, end="")
        printf(item["model"])
        offset = " " * 2
        printf(offset + "link: ", color=Colors.BRIGHT_GREEN, end="")
        printf(item["link"])
        printf(offset + "reviews: ", color=Colors.BRIGHT_GREEN, end="")
        offset = " " * 4
        good_reviews = []
        for j2, review in enumerate(item["reviews"]):
            if len(good_reviews) == 3: break
            if ranks[j1][j2] >= 4 and review["desc"] != "No description": good_reviews.append(review)
        if len(good_reviews) == 0: printf("No reviews found\n", color=Colors.ERROR)
        else:
            for review in good_reviews:
                printf(f"\n{offset}{review["name"]} ({review["rating"]}*):\n{offset}{review["desc"]}")
        i += 1


async def processRequest(command: str):
    command, args = command.split(" ", maxsplit=1)
    printf("magic happens here", color=Colors.HEADER)
    processed_input = agent1().process_input(args)
    if processed_input in Errors.AGENT1_NULL.value.replace("@#$%^", args):
        printf("An error occurred when processing user input.", Colors.ERROR)
        raise ValueError
    models = agent2().process_query(processed_input)
    items = await agent2_to_reviews(eval(models))
    rankingsAwait = [asyncio.to_thread(agent3().process_reviews, item["reviews"]) for item in items]
    rankings = await asyncio.gather(*rankingsAwait)
    print_tovars(items, rankings)


async def agent2_to_reviews(tovars: list[dict]):
    catalogAwait = await parseItems(tovars, Market.WILDBERRIES)
    catalog = []
    for model in catalogAwait:
        if model is None: continue
        catalog.extend(model[:3])
        if len(catalog) >= 9: break
    reviews = await parseReviews(catalog, Market.WILDBERRIES)
    items = []
    for item, item_reviews in zip(catalog, reviews):
        if item_reviews is None: continue
        REVIEWS = list()
        for review in item_reviews:
            REVIEW = dict()
            REVIEW["name"] = review[0]
            REVIEW["rating"] = review[1]
            REVIEW["desc"] = review[2]
            REVIEWS.append(REVIEW)
        ITEM = dict()
        ITEM["model"] = item[0]
        ITEM["link"] = item[1]
        ITEM["reviews"] = REVIEWS
        items.append(ITEM)
    return items

if __name__ == '__main__':
    start()

from server.agent1 import *
from server.agent2 import *
from server.agent3 import *


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
                    command, args = command.split(" ", maxsplit=1)
                    printf("magic happens here", color=Colors.HEADER)
                    res = agent1().process_input(args)
                    if res in Errors.AGENT1_NULL.value.replace("@#$%^", args):
                        printf("An error occurred when processing user input.", Colors.ERROR)
                        raise ValueError
                    agent2().process_query(res)
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


def print_tovars(tovars: list[dict]):
    i = 1
    for item in tovars:
        offset = " " * 2
        printf(f"{i}.", end="")
        printf(offset + f"model: ", color=Colors.BRIGHT_GREEN, end="")
        printf(item["model"])
        offset = " " * (len(str(i)) + 3)
        printf(offset + f"link: ", color=Colors.BRIGHT_GREEN, end="")
        printf(item["link"])
        printf(offset + f"reviews: ", color=Colors.BRIGHT_GREEN, end="")
        offset += " " * 2
        j = 1
        for review in item["reviews"]:
            if review["ranking"] >= 4:
                printf(offset + f"{j}.\n{review}")
                j += 1
        i += 1

if __name__ == '__main__':
    start()

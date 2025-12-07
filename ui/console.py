from enum import Enum
from server.agent_model import process_input, process_query
class Colors(Enum):
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Styles
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'


    #Aliases
    HEADER = BRIGHT_MAGENTA
    ERROR = BRIGHT_RED
    ENDL = RESET
    COMMAND = BRIGHT_CYAN
    TEXT = BRIGHT_WHITE

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
                    res = process_input(args)
                    if res: process_query(res)
                    else: printf("Something gone wrong. Try again.")
                case "-h":
                    print_help_message()
                case _:
                    raise ValueError("invalid input")
        except ValueError:
            printf("invalid input. Try again", Colors.ERROR)

        print_commands(["-f <description>", "-q"], ["find some item", "quit"])
        command = input()
    print("Thanks for using, see you next time!")

#-f Найди чайник 2кВт от 1000 до 5000 рублей


def print_commands(commands: list[str], descriptions: list[str]):
    print("commands:")
    offset = max(map(len, commands))
    for com, descr in zip(commands, descriptions):
        printf(com, end=('\t' * ((offset - len(com) + 3) // 4 + 1)), color=Colors.COMMAND)
        printf(descr)


def printf(message: str, color: Colors = Colors.TEXT, end='\n', ):
    print(color.value + message + Colors.ENDL.value, end=end)


def print_help_message():
    printf( "MANUAL:\nto search type -f and provide some description (e. g. \"-f find a powerful hair dryer "
            "between 20 and 50 bucks\")\n\nto exit program type -q", color=Colors.TEXT)


if __name__ == '__main__':
    start()

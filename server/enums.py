from enum import Enum

class Market(Enum):
    WILDBERRIES = ('p[class="feedback__header"]', 'span[class*="feedback__rating stars-line"]', 'span[class="feedback__text--item"]', 'ul[class="comments__list"]', 'span[class="product-card__name"]', 'a[href*="https://www.wildberries.ru/catalog/"]', 'div[class="product-card-list"]', 'https://www.wildberries.ru/catalog/0/search.aspx?search="{}"', 'div[class*="catalog-page__not-found"]')

class Errors(Enum):
    AGENT1_NULL = '''{
  "preprocessed": "@#$%^",
  "item_name": null,
  "model": null,
  "price_lower_bound": null,
  "price_upper_bound": null,
  "color": null,
  "size": null,
  "quick_delivery": null,
  "other_specs": null
}'''

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

    # Aliases
    HEADER = BRIGHT_MAGENTA
    ERROR = BRIGHT_RED
    ENDL = RESET
    COMMAND = BRIGHT_CYAN
    TEXT = BRIGHT_WHITE

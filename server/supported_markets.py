from enum import Enum

class Market(Enum):
    WILDBERRIES = ('p[class="feedback__header"]', 'span[class*="feedback__rating stars-line"]', 'span[class="feedback__text--item"]', 'ul[class="comments__list"]')
    OZON = ('span[class="l2l_28"]', '', 'span[class="l5o_28"]', 'div[class="mn5_28"]')
    YANDEXMARKET = ('', '', '', '')
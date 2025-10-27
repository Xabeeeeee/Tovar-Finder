from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contextlib import contextmanager
import time

link = ''
name_mask = 'p[class="feedback__header"]'
rating_mask = 'span[class*="feedback__rating stars-line"]'
description_mask = 'span[class="feedback__text--item"]'
reviews_mask = 'ul[class="comments__list"]'

needed_reviews = 500

HTML_fetchTag = lambda parent, css_selector: parent.find_elements(By.CSS_SELECTOR, css_selector)

def getName(review) -> str:
    try:
        name = HTML_fetchTag(review, name_mask)[0].text
    except:
        name = "Anonymous"
    return name


def getRating(review) -> str:
    try:
        rating = HTML_fetchTag(review, rating_mask)[0].get_attribute('class')[-1]
    except:
        rating = "-"
    return rating


def getDescription(review) -> str:
    try:
        description = HTML_fetchTag(review, description_mask)[0].text
    except:
        description = "No description"
    return description


def JSscroller(webpage, elementmask, target, maxatts, delay):
    atts, lenprevious, stagnation = 0, 0, 0
    reviewslist = webpage.find_element(By.CSS_SELECTOR, elementmask)
    while atts < maxatts:
        try:
            lencurrent = len(reviewslist.find_elements(By.XPATH, './*'))
            if lencurrent >= target:
                break
            if lencurrent == lenprevious:
                stagnation += 1
                if stagnation >= 3:
                    break
            else:
                stagnation = 0
            lenprevious = lencurrent
            webpage.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)
            atts += 1
        except:
            break
    return reviewslist


@contextmanager
def generateDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        yield driver
    finally:
        driver.quit()


def main():
    with generateDriver() as driver:
        try:
            url = link
            driver.get(url)
            driver.maximize_window()
            time.sleep(3)

            reviews = JSscroller(
                webpage=driver,
                elementmask=reviews_mask,
                target=needed_reviews,
                maxatts=50,
                delay=0.5
            )

            for review in reviews.find_elements(By.XPATH, './*'):
                try:
                    name = getName(review)
                    rating = getRating(review)
                    description = getDescription(review)
                    print(" / ".join([name, rating, description]))
                except:
                    print(f"Failed to process review")

        except:
            print(f"Failed to load page")


if __name__ == "__main__":
    main()
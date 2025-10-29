from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .supported_markets import Market
from contextlib import contextmanager
import time

MAX_ATTEMPTS = 50
STAGNATION_ATTEMPTS = 3
TIMEOUT = 10
LOAD_DELAY = 0.5
NEEDED_REVIEWS = 500

HTML_fetchTag = lambda parent, css_selector: parent.find_elements(By.CSS_SELECTOR, css_selector)
HTML_findTag = lambda parent, css_selector: parent.find_element(By.CSS_SELECTOR, css_selector)

@contextmanager
def Driver():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()
        yield driver
    finally:
        if driver:
            driver.quit()

def processReviews(reviews, market : Market):

    name_mask, rating_mask, description_mask = market.value[0], market.value[1], market.value[2]

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

    for review in reviews.find_elements(By.XPATH, './*'):
        try:
            name = getName(review)
            rating = getRating(review)
            description = getDescription(review)
            yield name, rating, description
        except:
            print("Failed to process review")

def reviewParser(link : str, market : Market):

    reviews_mask = market.value[3]

    def JSscroller(webpage):
        atts, len_previous, stagnation = 0, 0, 0
        reviews_list = HTML_findTag(webpage, reviews_mask)
        while atts < MAX_ATTEMPTS:
            try:
                len_current = len(reviews_list.find_elements(By.XPATH, './*'))
                if len_current >= NEEDED_REVIEWS:
                    break
                if len_current == len_previous:
                    stagnation += 1
                    if stagnation >= STAGNATION_ATTEMPTS:
                        break
                else:
                    stagnation = 0
                len_previous = len_current
                webpage.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(LOAD_DELAY)
                atts += 1
            except:
                break
        return reviews_list

    try:
        with Driver() as driver:
            driver.get(link)
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, reviews_mask))
            )
            reviews = JSscroller(driver)
            return list(processReviews(reviews, market))
    except:
        print("Failed to load page")
        return None
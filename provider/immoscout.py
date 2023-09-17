import logging

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def write_immoscout_token():
    logger.debug("starting...")
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1024,768")
    driver = uc.Chrome(options=chrome_options)
    attempt = 0
    new_token = None
    while attempt <= 5:
        attempt += 1
        try:
            logger.debug("loading page ...")
            driver.get(
                'https://www.immobilienscout24.de/Suche/de/schleswig-holstein/pinneberg-kreis/haus-mieten?numberofrooms=3.0-&price=-2000.0&livingspace=65.0-&pricetype=rentpermonth&enteredFrom=one_step_search')
            logger.debug("page loaded...")
            try:
                logger.debug("waiting for captcha box...")
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "captcha-box"))).click()
                logger.debug("captcha box was clicked...")
            except TimeoutException:
                if "roboter" in driver.title.lower():
                    logger.debug("cannot find captcha box...")
                    continue

            logger.debug("waiting for cookie...")
            reese_token = WebDriverWait(driver, timeout=20).until(lambda d: d.get_cookie('reese84'))['value']
            logger.debug(f"reese84 cookie found: {reese_token}")
            new_token = f"reese84={reese_token}"
            break
        except TimeoutException:
            logger.debug(f"detected as robot. current attempt: {attempt}")
            continue
    driver.quit()
    logger.debug("SUCCESS! driver quiting...")
    f = open("/home/pi/dev/crawl/immoscout24-token-provider/cookie.txt", "w")
    f.write(new_token)
    f.close()

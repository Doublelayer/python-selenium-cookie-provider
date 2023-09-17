import logging
import os
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import undetected_chromedriver as uc

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY'] = '/run/user/1000/gdm/Xauthority'


def write_immonet_token():
    logger.debug("starting to get and write immonet token")
    driver = uc.Chrome(version_main=113, headless=False)
    driver.maximize_window()
    attempt = 0
    new_token = None
    while attempt <= 5:
        attempt += 1
        try:
            driver.get(
                'https://www.immonet.de/immobiliensuche/beta?sortby=0&suchart=1&objecttype=1&marketingtype=2&parentcat=1&locationname=Hamburg&locationIds=150697')
            time.sleep(10)

            item = driver.execute_script(
                '''return document.querySelector('div#usercentrics-root').shadowRoot.querySelector('button[data-testid="uc-accept-all-button"]')''')
            item.click()

            reese_token = f"{driver.get_cookie('uids')['value']}"
            logger.debug(reese_token)
            new_token = reese_token
            break
        except TimeoutException:
            logger.debug(f"detected as robot. current attempt: {attempt}")
            continue
    driver.quit()
    logger.debug("driver quit")
    f = open("/home/pi/dev/crawl/immoscout24-token-provider/immonet-cookie.txt", "w")
    f.write(new_token)
    f.close()


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


if __name__ == '__main__':
    write_immoscout_token()
    # write_immonet_token()

    # Warte bis zur nächsten vollen Viertelstunde
    # next_call = (datetime.datetime.now() + datetime.timedelta(minutes=13)).replace(second=0, microsecond=0)
    #
    # # Schleife, die die Methode alle 15 Minuten ausführt
    # while True:
    #     # Berechne die Zeitdauer bis zum nächsten Aufruf
    #     sleep_duration = (next_call - datetime.datetime.now()).total_seconds()
    #
    #     # Warte bis zum nächsten Aufruf
    #     time.sleep(sleep_duration)
    #
    #     # Rufe die Methode auf
    #     write_token()
    #
    #     # Berechne die Zeit für den nächsten Aufruf
    #     next_call = (next_call + datetime.timedelta(minutes=13)).replace(second=0, microsecond=0)

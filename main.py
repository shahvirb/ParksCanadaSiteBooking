from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium

START_URL = r'https://reservation.pc.gc.ca/create-booking/results?resourceLocationId=-2147483543&mapId=-2147483199&searchTabGroupId=2&bookingCategoryId=1&startDate=2023-08-05&endDate=2023-08-07&nights=2&isReserving=true&partySize=6&filterData=%7B%22-32756%22:%22%5B%5B1%5D,0,0,0%5D%22%7D&searchTime=2023-03-17T13:26:34.393'

WAIT_SEC = 5

def make_browser(url: str) -> webdriver.Chrome:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    return driver


def wait_and_get_elements(driver, xpath, wait=WAIT_SEC, until=EC.presence_of_element_located):
    try:
        WebDriverWait(driver, wait).until(until((By.XPATH, xpath)))
        return driver.find_elements(By.XPATH, xpath)
    except selenium.common.exceptions.TimeoutException:
        return None


def click_list_view(driver):
    VIEW_BUTTONS = r'//div[@class="btn-search-results-toggle-label"]'
    # the list view button is the second of these
    wait_and_get_elements(driver, VIEW_BUTTONS)[1].click()


def expand_list_item(driver, i:int):
    """
    :param driver:
    :param x: the index of the list item to click
    :return:
    """
    items = wait_and_get_elements(driver, r'//*[@class="resource-name"]')
    items[i].click()

def click_reserve(driver, i:int):
    """
    :param driver:
    :param i: the index of the list item used by expand_list_item on which to click reserve
    :return:
    """
    reserve_btn = wait_and_get_elements(driver, f'//button[@id="reserveButton-{i}"]')[0]
    reserve_btn.click()


if __name__ == '__main__':
    driver = make_browser(START_URL)
    driver.implicitly_wait(0)

    # driver.execute_script("window.open()")
    # driver.switch_to.window(driver.window_handles[1])
    # driver.get("https://google.com")

    SITE_TO_RESERVE = 0

    click_list_view(driver)
    expand_list_item(driver, SITE_TO_RESERVE)
    while True:
        click_reserve(driver, SITE_TO_RESERVE)
        if wait_and_get_elements(driver, r'//app-reserve-restriction-dialog', 3, until=EC.visibility_of_element_located):
            #close = driver.find_element(By.XPATH, r'//app-reserve-restriction-dialog//button')
            #close = wait_and_get_elements(driver, r'//app-reserve-restriction-dialog//button', 10, until=EC.element_to_be_clickable)
            close = wait_and_get_elements(driver, r'//app-reserve-restriction-dialog//button', 10)
            if close:
                close[0].click()
                print('RESTRICTED')
            else:
                print('Did not find close button but found app-reserve-restriction-dialog')

    # TODO should we catch and ignore exceptions so they don't kill the browser if something goes wrong?
    # TODO can we detach the browser from python before exiting so that if python crashes the browser is still intact in case the user has reserved the site and is now entering in reservation info?

    input("Press any key to exit")

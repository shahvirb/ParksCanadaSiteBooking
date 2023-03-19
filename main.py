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

def wait_and_get_elements(driver, xpath, wait=WAIT_SEC):
    try:
        WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_elements(By.XPATH, xpath)
    except selenium.common.exceptions.TimeoutException:
        return None

def click_list_view(driver):
    LIST_VIEW = r'//div[@class="btn-search-results-toggle-label"]'
    wait_and_get_elements(driver, LIST_VIEW)[1].click()

def reserve_list_item(driver, x:int):
    items = wait_and_get_elements(driver, r'//*[@class="resource-name"]')
    items[x].click()
    reserve_btn = wait_and_get_elements(driver, f'//button[@id="reserveButton-{x}"]')[0]
    reserve_btn.click()

if __name__ == '__main__':
    driver = make_browser(START_URL)

    # driver.execute_script("window.open()")
    # driver.switch_to.window(driver.window_handles[1])
    # driver.get("https://google.com")

    click_list_view(driver)
    # click the first resource
    while True:
        reserve_list_item(driver, 1)
        if wait_and_get_elements(driver, r'//app-reserve-restriction-dialog', 1):
            close = driver.find_element(By.XPATH, r'//app-reserve-restriction-dialog//button')
            close.click()
            print('RESTRICTED')

    input("Press any key to exit")


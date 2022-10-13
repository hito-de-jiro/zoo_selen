import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


URL = f'https://www.zooplus.de/tierarzt/results?animal_99=true'

num_page = 3
i = 1
browser = webdriver.Chrome()
browser.implicitly_wait(3)

while i <= num_page:
    try:
        browser.get(URL + '&page=' + str(i))
        # browser.switch_to.active_element.find_element(By.XPATH,
        #                                                      "/html/body/div[2]/div[3]/div/div/div[2]/div/div/button[2]").click()
        WebDriverWait(browser, 3).until(
            ec.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/div/div/button[2]"))).click()

    except TimeoutException:
        pass
    finally:
        time.sleep(3)

    i += 1

browser.close()
browser.quit()
print('Done!')

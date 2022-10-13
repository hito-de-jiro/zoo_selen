#!python3
import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

HOST = 'https://www.zooplus.de'
URL = f'https://www.zooplus.de/tierarzt/results?animal_99=true'


def get_html(url=URL):
    """Starts the browser, receives and returns raw data"""
    # Creating a list to collect raw data
    all_data = []
    num_page = 3    # Number of pages to parse
    i = 1
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    while i <= num_page:
        browser.get(url + '&page=' + str(i))
        print('Parsing the page # %s' % i)
        try:
            WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.XPATH,
                                                                        "/html/body/div[2]/div[3]/div/div/div[2]"
                                                                        "/div/div/button[2]"))).click()
        except TimeoutException:
            pass
        finally:
            elems = browser.find_elements(By.CLASS_NAME, 'result-intro ')
            #  get value from list of elems
            for elem in elems:
                # make empty list and record data elements
                get_data = []
                empty_string = 'empty value'
                title = elem.find_element(By.CLASS_NAME, 'result-intro__title')
                get_data.append(title.text)
                rating = elem.find_element(By.CLASS_NAME, 'result-intro__rating__note')
                get_data.append(rating.text)
                try:
                    description = elem.find_element(By.CLASS_NAME, 'result-intro__subtitle')
                    get_data.append(description.text)
                except NoSuchElementException:
                    get_data.append(empty_string)

                try:
                    working_time = elem.find_element(By.CLASS_NAME, 'daily-hours__range')
                    get_data.append(working_time.text)
                except NoSuchElementException:
                    get_data.append(empty_string)

                try:
                    working_time_note = elem.find_element(By.CLASS_NAME, 'daily-hours__note').text
                    get_data.append(working_time_note)
                except NoSuchElementException:
                    get_data.append(empty_string)

                address_text = elem.find_element(By.CLASS_NAME, 'result-intro__address').text
                address = address_text.replace('\n', '')
                get_data.append(address)
                # record list 'get_data' in dict 'all_data'
                all_data.append(get_data)
        print(f'Parsing the page # {i} successfully completed.')
        i += 1

    print('Done!')
    time.sleep(5)
    browser.close()
    browser.quit()
    return all_data


def save_csv(data):
    """Create and record CSV-file"""
    csv_file = open('output_data.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data)
    csv_file.close()


def main(url=URL):
    data = get_html(url)
    save_csv(data)
    print('Welldone!')


if __name__ == '__main__':
    main()

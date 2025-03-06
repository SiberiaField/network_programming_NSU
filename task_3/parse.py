from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd


options = webdriver.FirefoxOptions()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)

wait = WebDriverWait(driver, 3)

flowers_info_table = {'flower_name': [], 'price': []}


def parse_page():
    flowers_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.products-view')))
    flower_idx = 1
    while 1:
        try:
            flower_view_item = flowers_list.find_element(By.CSS_SELECTOR, f'div.products-view-block:nth-child({flower_idx}) > div:nth-child(1)')
        except NoSuchElementException:
            print(f"has parsed {flower_idx - 1} flowers")
            break

        flower_view_name = flower_view_item.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div:nth-child(1)')
        flowers_info_table['flower_name'].append(flower_view_name.text)

        flower_view_price_data = flower_view_item.find_element(By.CLASS_NAME, 'products-view-price-data')
        flower_view_price = flower_view_price_data.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(1)')
        flower_price = flower_view_price.find_element(By.CLASS_NAME, 'price')
        flower_price_current = flower_price.find_element(By.CSS_SELECTOR, 'div:nth-child(1)')
        flower_price_number = flower_price_current.find_element(By.CLASS_NAME, 'price-number')
        flowers_info_table['price'].append(flower_price_number.text)

        flower_idx += 1


def main():
    page_idx = 1
    while 1:
        driver.get(f'https://driedflowershop.ru/categories/katalog?page={page_idx}')
        print(f'Page {page_idx} - ', end='', sep='')
        try:
            parse_page()
        except TimeoutException:
            print("parsing is completed")
            break
        except Exception as unexpected_e:
            print(f" unxpected exception!\n{unexpected_e}")
            break

        page_idx += 1

    df = pd.DataFrame(flowers_info_table)
    df.to_csv('flowers_info.csv')

    driver.quit()


main()

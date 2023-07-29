from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.amazon.in")
driver.maximize_window()

search_box = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
search_box.send_keys("smartphone under 25k")

search_button = driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]')
search_button.click()

search_button = driver.find_element(By.XPATH, '//span[text()="Samsung"]')
search_button.click()

phone_name_list = []
phone_price_list = []
phone_url_list = []
phone_ratings_list = []

while True:
    try:
        products = driver.find_elements(By.XPATH, "//div[@class='a-section']")
        print("Number of products on this page:", len(products))  # Debugging statement
        for phone in products:
            try:
                phone_name = phone.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']").text
                phone_price = phone.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
                phone_url = phone.find_element(By.XPATH, ".//a[@class='a-link-normal s-no-outline']").get_attribute("href")
                phone_ratings = phone.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text
                
                phone_name_list.append(phone_name)
                phone_price_list.append(phone_price)
                phone_url_list.append(phone_url)
                phone_ratings_list.append(phone_ratings)
                
            except NoSuchElementException:
                continue
    except StaleElementReferenceException:
        print("Stale element encountered. Refreshing the page...")  # Debugging statement
        driver.refresh()
        time.sleep(3)
        continue

    try:
        next_button = driver.find_element(By.XPATH, "//span[@class='s-pagination-strip']/a[contains(text(),'Next')]")
        next_button.click()
        time.sleep(3)
    except NoSuchElementException:
        print("No 'Next' link found. We have reached the last page of results.")  # Debugging statement
        break

df_products = pd.DataFrame({
    'phone_name': phone_name_list,
    'phone_price': phone_price_list,
    'phone_url': phone_url_list,
    'phone_ratings': phone_ratings_list
})

df_products.to_csv('phone_details.csv', index=False)

driver.quit()

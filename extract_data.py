# Importing the necessary libraries
from selenium import webdriver  # Used to automate web browser interaction
from selenium.webdriver.common.by import By  # Helps in locating elements on web pages
import pandas as pd  # Pandas library for data manipulation and analysis
import time

# Creating an empty DataFrame with specified columns
# This DataFrame will be used to store the scraped data
df = pd.DataFrame(columns=['name', 'price', 'score'])

# Initializing the Chrome WebDriver
# This opens up a Chrome browser window for web scraping
driver = webdriver.Chrome()

BASE_URL = "https://www.trivago.es/en-US/lm/hotels-barcelona-spain?search=200-13437;dr-20240629-20240630"

first_page = True

page_num = 1
max_pages = 1
duplicated = False
while page_num <= max_pages:
    url = BASE_URL + ";pa-" + str(page_num)
    driver.get(url)  # Navigating to the constructed URL in the browser

    time.sleep(10)

    if first_page:
        try:
            #allow_all_button = driver.find_element(By.XPATH, '//*[@id="uc-center-container"]/div[2]/div/div[1]/div/button[3]')
            #allow_all_button.click()
            #time.sleep(10)
            datos = driver.find_elements(By.XPATH, '//ol[@data-testid="pagination"]')[0].text
            max_pages = int(datos.split('\n')[-1])
        except Exception as e:
            max_pages = 16
        first_page = False

    names = driver.find_elements(By.XPATH, '//button[@data-testid="item-name"]') # separar por comas y coger la posicion -2 del array resultante
    prices = driver.find_elements(By.XPATH, '//span[@data-testid="recommended-price"]')
    scores = driver.find_elements(By.XPATH, '//span[@itemprop="ratingValue"]')

    # Extracting the text from each player element and storing in a list
    name_list = [name.text.replace(",", "") for name in names]
    price_list = [price.text.replace(",", "").replace("€", "") for price in prices]
    score_list = [score.text.replace(",", "") for score in scores]
    
    # Pairing each player's name with their salary and year using the zip function
    data_tuples = list(zip(name_list[1:], price_list[1:], score_list[1:]))
    
    temp_df = pd.DataFrame(data_tuples, columns=['name', 'price', 'score'])
    df = pd.concat([df,temp_df], ignore_index=True)
    print(page_num)
    page_num += 1

print(df)
nombre_archivo = 'datos.csv'
df.to_csv(nombre_archivo, index=False)
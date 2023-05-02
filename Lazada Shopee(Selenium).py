#pip install webdriver-manager

#2. Web Scrapping with Selenium
#Import all the necessary libraries. Pandas and the Selenium webdriver are the main libraries for simple web scraping.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

#Data manipulation
import pandas as pd
import time

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

#After importing the libraries, the next step is to initiate the Chrome driver. The Chrome browser should open in a new empty window since there is no feed URL.

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#Scraping Lazada
#The target feed URL is saved as Lazada_url. It will open Lazada e-commerce platform and search for the item specified.

Lazada_url = 'https://www.lazada.com.my'
search_item = 'Nestle Honey Stars 150g'
driver.get(Lazada_url)

p = driver.find_element(By.ID, 'q')
p.send_keys(search_item)
p.submit()

#Once the feed URL is entered, the target website will be opened. The following process is to find the name and price of our search item. In Selenium, you can find the HTML elements by the using Class name methods.
item_titles = driver.find_elements(By.CLASS_NAME, 'RfADt')
item_prices = driver.find_elements(By.CLASS_NAME, 'ooOxS')

# Initialize empty lists
titles_list = []
prices_list = []

# Loop over the item_titles and item_prices
for title in item_titles:
    titles_list.append(title.text)
for price in item_prices:
    prices_list.append(price.text)

#After scraping this page, we will proceed to the next page. XPath is used because the next page button has two classes and the find element by class name method only finds elements from one class. We must also tell the browser what to do if the next page button is disabled. If the button is disabled, the browser closes. If not disabled, it will move to the next page, requiring another scrape. Our search yielded 25 results on one page, thus concluding our scraping procedure.
try:
    driver.find_element('xpath','//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[3]/button/span/svg').click()
except NoSuchElementException: 
    driver.quit()

#Lastly, save the data in the data frame.


dfL = pd.DataFrame(zip(titles_list, prices_list), columns=['ItemName', 'Price'])
print('Lazada data frame: \n', dfL.head())

#Scraping Shopee
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
Shopee_url = 'https://shopee.com.my/'
driver.get(Shopee_url)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH,'//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button'))).click()

try:
    time.sleep(3)
    close_btn = driver.execute_script('return document.querySelector("#shopee-banner-popup-stateful").shadowRoot.querySelector("div.home-popup__close-area div.shopee-popup__close-btn")')
    close_btn.click()
except:
    pass

p = driver.find_element(By.CLASS_NAME, 'shopee-searchbar-input__input')
p.send_keys(search_item)
driver.find_element('xpath', '//*[@id="main"]/div/header/div[2]/div/div[1]/div[1]/button').click()

item_titles2 = driver.find_elements(By.CLASS_NAME, 'dpiR4u')
item_prices2 = driver.find_elements(By.CLASS_NAME, 'ZEgDH9')

#Initialize empty lists
titles_list2 = []
prices_list2 = []

#Loop over the item_titles and item_prices
for title in item_titles2:
    titles_list2.append(title.text)
for price in item_prices2:
    prices_list2.append(price.text)

scroll_pause_time = 1

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, window.scrollY + 500);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
 
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, window.scrollY + 500);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue

#close driver
try:
    driver.find_element('xpath','//*[@id="main"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div/button[3]/svg').click()
except NoSuchElementException: 
    driver.quit()

dfS = pd.DataFrame(zip(titles_list2, prices_list2), columns=['ItemName', 'Price'])
print('Shopee data frame: \n', dfS.head())

#3. Data Cleaning and Preparation
#dfL.info() shows that the Price column type is object, not float as each Price column entry contains the currency symbol "RM" (Malaysian Ringgit). If the Price column is not integer or float, we cannot extract statistical features from it. We will also change the ItemName column to string.

print(dfL.info())

#We need to remove the currency symbol and convert the entire column into a float type

dfL['Price'] = dfL['Price'].str.replace('RM', '').astype(float)
dfS['Price'] = dfS['Price'].astype(float)


#Then we will remove any irrelevant entries
dfL = dfL[dfL['ItemName'].str.contains('Starbucks') == False]
dfL = dfL[dfL['ItemName'].str.contains('Cornflake') == False]
dfL = dfL[dfL['ItemName'].str.contains('CORNFLAKE') == False]
i=0

for x in dfS['ItemName']:
    dfS['ItemName'][i] = dfS['ItemName'].str.rsplit('\n')[i][:-2]   
    if dfS['ItemName'][i] == []:
        dfS['ItemName'][i] = 'Nestle Honey Stars 150g'
    i+=1

#Additionally, we will create a column titled Platform and assign "Lazada" and "Shopee" respectively to each entry in this column. This is done so that we can group the entries by platform (Lazada and Shopee) when we compare prices between the two platforms later.
dfL['Platform'] = 'Lazada'
dfS['Platform'] = 'Shopee'

#We export the data to a csv file.

dfL.to_csv('Honey Stars Lazada.csv')
dfS.to_csv('Honey Stars Shopee.csv')

#4. Visualization and Analysis
# Plot the chart
sns.set()
_ = sns.boxplot(x='Platform', y='Price', data=dfL)
_ = plt.title('Comparison of Nestle Honey Stars 150g prices between e-commerce platforms in Malaysia')
_ = plt.ylabel('Price (RM)')
_ = plt.xlabel('E-commerce Platform')
# Show the plot
plt.show()

#For Lazada, the prices of the items range from RM6 to RM20, with the median price falling between RM7 and RM8. The box also has slightly longer whiskers, indicating that the prices are relatively inconsistent with significant outliers.
# Plot the chart
sns.set()
_ = sns.boxplot(x='Platform', y='Price', data=dfS)
_ = plt.title('Comparison of Nestle Honey Stars 150g prices between e-commerce platforms in Malaysia')
_ = plt.ylabel('Price (RM)')
_ = plt.xlabel('E-commerce Platform')
# Show the plot
plt.show()

#original code inspired by https://github.com/drshahizan
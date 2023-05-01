import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

ZILLOW_URL = "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
CHROME_DRIVER_PATH = "D:\Python course\chromedriver_win32\chromedriver.exe"
# Enter the form url you created.
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSerEw4tdoewZSnGMkDwHOPI3BjdoetM4VCy06MXW1LBD224oQ/viewform"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(ZILLOW_URL, headers=headers)
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')

information = soup.find('script', {"data-zrr-shared-data-key": "mobileSearchPageStore"}).text.strip("<!--").strip("-->")
information_dict = json.loads(information)
house_result_dict = information_dict['cat1']['searchResults']['listResults']

links = []
address_list = []
prices = []
for listing in house_result_dict:
    links.append(listing['detailUrl'])
    address_list.append(listing['address'])
    try:
        prices.append(listing['price'].split("+")[0])
    except KeyError:
        prices.append(listing['units'][0]['price'].split("+")[0])

all_link_list = []
for link in links:
    if "http" not in link:
        all_link_list.append(f"https://www.zillow.com{link}")
    else:
        all_link_list.append(link)

price_list = [price.split("/mo")[0] for price in prices]

print(all_link_list)
print(address_list)
print(price_list)

driver = webdriver.Chrome(service=Service(executable_path=CHROME_DRIVER_PATH))

for n in range(len(all_link_list)):
    driver.get(GOOGLE_FORM_URL)

    time.sleep(3)
    address = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(address_list[n])

    price = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(price_list[n])

    link = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(all_link_list[n])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()


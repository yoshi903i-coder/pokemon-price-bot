from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

driver.get("https://www.cardrush-pokemon.jp/product-list?page=1")
import time
time.sleep(5)
soup = BeautifulSoup(driver.page_source, "html.parser")
items = soup.select(".item_box")
print("items: " + str(len(items)))
for item in items[:5]:
    name_el = item.select_one(".item_name")
    if name_el:
        print("name: " + name_el.text.strip())
driver.quit()

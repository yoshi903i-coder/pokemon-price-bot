from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

url = "https://cardrush.media/pokemon/buying_prices"
driver.get(url)
print("ページを開きました")
time.sleep(10)

print("=== ページタイトル ===")
print(driver.title)

print("=== ページソース（最初の3000文字）===")
print(driver.page_source[:3000])

driver.quit()

import requests
from bs4 import BeautifulSoup
import csv

# 調べたいURL（例：カードラッシュのポケカページ）
url = "https://www.cardrush-pokemon.jp/product-list"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.find_all("div", class_="product-item")

data = []

for card in cards:
    name = card.find("h3").text.strip()
    price = card.find("span", class_="price").text.strip()
    
    stock = "在庫あり"
    if "在庫切れ" in card.text:
        stock = "在庫切れ"
    
    print(name, price, stock)
    data.append([name, price, stock])

# CSV保存
with open("card_prices.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["カード名", "価格", "在庫"])
    writer.writerows(data)

print("完了！")

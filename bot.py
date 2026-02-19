import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

today = datetime.now().strftime("%Y-%m-%d %H:%M")
all_data = []
page = 1

while True:
    url = f"https://www.cardrush-pokemon.jp/product-list?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select(".item_box")
    if not items:
        break

    for item in items:
        name_el = item.select_one(".item_name")
        price_el = item.select_one(".price")
        stock_el = item.select_one(".soldout")

        name = name_el.text.strip() if name_el else "不明"
        price = price_el.text.strip().replace("¥","").replace(",","").replace("円","").strip() if price_el else "0"
        stock = "在庫切れ" if stock_el else "在庫あり"

        all_data.append([today, name, price, stock])

    page += 1
    if page > 100:
        break

df_new = pd.DataFrame(all_data, columns=["日時","カード名","価格","在庫"])

excel_path = "card_prices.xlsx"
if os.path.exists(excel_path):

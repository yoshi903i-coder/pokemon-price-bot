import requests
from bs4 import BeautifulSoup

url = "https://www.cardrush-pokemon.jp/product-list?page=1"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers, timeout=60)
soup = BeautifulSoup(res.text, "html.parser")

print("STATUS: " + str(res.status_code))

# クラス名を探す
classes = ["item_box", "item-box", "product_item", "product-item", "goods", "item"]
for c in classes:
    found = soup.select("." + c)
    print(c + ": " + str(len(found)) + "件")

# 最初の商品っぽいタグを探す
divs = soup.find_all("div", limit=5)
for d in divs:
    cls = d.get("class", [])
    if cls:
        print("div class: " + str(cls))

# ページソース最初の2000文字
print("=== HTML ===")
print(res.text[:2000])

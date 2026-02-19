import requests
from bs4 import BeautifulSoup

# 買い取りページのURLを試す
urls = [
    "https://www.cardrush-pokemon.jp/buy/product-list",
    "https://www.cardrush-pokemon.jp/buy",
    "https://www.cardrush-pokemon.jp/purchase/product-list",
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    res = requests.get(url, headers=headers, timeout=30)
    print(f"URL: {url}")
    print(f"ステータス: {res.status_code}")
    soup = BeautifulSoup(res.text, "html.parser")
    # クラス名を探す
    for cls in ["item_box", "item-box", "product-item", "goods_box", "buy_item"]:
        items = soup.select(f".{cls}")
        print(f"  クラス .{cls}: {len(items)}件")
    print("---")

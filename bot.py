import requests
from bs4 import BeautifulSoup
import re
import subprocess
from datetime import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter
import os

today_str = datetime.now().strftime("%Y-%m-%d")
now = datetime.now()
sheet_name = f"{now.year}-{now.month}"

all_data = []
page = 1

while True:
    url = f"https://www.cardrush-pokemon.jp/buy/product-list?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".item_box")
        if not items:
            break
        for item in items:
            name_el = item.select_one(".item_name")
            price_el = item.select_one(".price")
            stock_el = item.select_one(".soldout")
            full_name = name_el.text.strip() if name_el else "不明"

            state_match = re.search(r'【状態([^】]+)】', full_name)
            state = state_match.group(1) if state_match else ""

            rarity_match = re.search(r'\[([A-Za-z★☆◆\-]+)\]', full_name)
            rarity = rarity_match.group(1) if rarity_match else ""

            clean_name = re.sub(r'【状態[^】]+】', '', full_name).strip()

            price_text = price_el.text.strip() if price_el else "0"
            price_num = re.sub(r'[^\d]', '', price_text)
            price = int(price_num) if price_num else 0

            stock = "在庫切れ" if stock_el else "在庫あり"
            all_data.append({
                "カード名": clean_name,
                "レアリティ": rarity,
                "状態": state,
                "価格": price,
                "在庫": stock
            })
        print(f"ページ {page} 取得完了 ({len(all_data)}件)")
        page += 1
    except Exception as e:
        print(f"ページ {page} エラー: {e}")
        page += 1
        if page > 9999:
            break

print(f"合計取得件数: {len(all_data)}")

excel_path = "card_prices.xlsx"
if os.path.exists(excel_path):
    wb = load_workbook(excel_path)
else:
    wb = Workbook()
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

if sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
else:
    ws = wb.create_sheet(sheet_name)
    ws["A1"] = "カード名"
    ws["B1"] = "レアリティ"
    ws["C1"] = "状態"
    ws["D1"] = "在庫"

date_col = None
for col in range(5, ws.max_column + 2):
    val = ws.cell(row=1, column=col).value
    if val == today_str:
        date_col = col
        break
    elif val is None:
        ws.cell(row=1, column=col).value = today_str
        date_col = col
        break

existing_rows = {}
for row in range(2, ws.max_row + 1):
    key = (ws.cell(row=row, column=1).value, ws.cell(row=row, column=3).value)
    existing_rows[key] = row

next_row = max(ws.max_row + 1, 2)
for d in all_data:
    key = (d["カード名"], d["状態"])
    if key in existing_rows:
        r = existing_rows[key]
        ws.cell(row=r, column=2).value = d["レアリティ"]
        ws.cell(row=r, column=4).value = d["在庫"]
        ws.cell(row=r, column=date_col).value = d["価格"]
    else:
        ws.cell(row=next_row, column=1).value = d["カード名"]
        ws.cell(row=next_row, column=2).value = d["レアリティ"]
        ws.cell(row=next_row, column=3).value = d["状態"]
        ws.cell(row=next_row, column=4).value = d["在庫"]
        ws.cell(row=next_row, column=date_col).value = d["価格"]
        existing_rows[key] = next_row
        next_row += 1

if "グラフ用" not in wb.sheetnames:
    wg = wb.create_sheet("グラフ用")
    wg["A1"] = "カード名を入力:"
    wg["B1"] = ""
    wg["A2"] = "開始日（例: 2026-02-19）:"
    wg["B2"] = ""
    wg["A3"] = "終了日（例: 2026-02-28）:"
    wg["B3"] = ""
    wg["A5"] = "↓ここに抽出データが表示されます"
    wg["A6"] = "日付"
    wg["B6"] = "価格"

wb.save(excel_path)
print("Excel保存完了！")

subprocess.run(["git", "config", "user.email", "bot@example.com"])
subprocess.run(["git", "config", "user.name", "PriceBot"])
subprocess.run(["git", "add", "card_prices.xlsx"])
subprocess.run(["git", "commit", "-m", f"価格更新 {today_str}"])
subprocess.run(["git", "push"])
print("GitHubにアップロード完了！")

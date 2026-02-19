import requests
from bs4 import BeautifulSoup
import re
import subprocess
from datetime import datetime
from openpyxl import load_workbook, Workbook
import os
import time

today_str = datetime.now().strftime("%Y-%m-%d")
now = datetime.now()
sheet_name = f"{now.year}-{now.month}"

all_data = []
page = 1

while True:
    url = f"https://www.cardrush-pokemon.jp/product-list?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=60)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".item_box")
        if not items:
            print(f"ページ{page}で終了")
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
            clean_name = re.sub(r'【状態[^】]+】', '', full_name)
            clean_name = re.sub(r'\[[^\]]+\]', '', clean_name).strip()
            price_text = price_el.text.strip() if price_el else "0"
            price_num = re.sub(r'[^\d]', '', price_text)
            price = int(price_num) if price_num else 0
            buy_price = int(price * 0.8)
            stock_status = "在庫切れ" if stock_el else "在庫あり"
            all_data.append({
                "カード名": clean_name,
                "レアリティ": rarity,
                "状態": state,
                "在庫状況": stock_status,
                "販売価格": price,
                "買取予想": buy_price,
            })
        print(f"ページ{page} 完了 合計{len(all_data)}件")
        page += 1
        time.sleep(1)
    except Exception as e:
        print(f"ページ{page} エラー: {e} → スキップして次へ")
        page += 1
        time.sleep(3)
    if page > 9999:
        break

print(f"取得完了: {len(all_data)}件")

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
    ws["D1"] = "在庫状況"

date_col = None
col = 5
while True:
    val = ws.cell(row=1, column=col).value
    if val == today_str + "_販売":
        date_col = col
        break
    elif val is None:
        ws.cell(row=1, column=col).value = today_str + "_販売"
        ws.cell(row=1, column=col+1).value = today_str + "_買取予想"
        ws.cell(row=1, column=col+2).value = today_str + "_前日価格比率"
        ws.cell(row=1, column=col+3).value = today_str + "_前日価格増減"
        date_col = col
        break
    col += 4

existing_rows = {}
for row in range(2, ws.max_row + 1):
    key = (ws.cell(row=row, column=1).value, ws.cell(row=row, column=3).value)
    existing_rows[key] = row

next_row = max(ws.max_row + 1, 2)

for d in all_data:
    key = (d["カード名"], d["状態"])
    if key in existing_rows:
        r = existing_rows[key]
    else:
        ws.cell(row=next_row, column=1).value = d["カード名"]
        ws.cell(row=next_row, column=2).value = d["レアリティ"]
        ws.cell(row=next_row, column=3).value = d["状態"]
        ws.cell(row=next_row, column=4).value = d["在庫状況"]
        r = next_row
        existing_rows[key] = next_row
        next_row += 1
    ws.cell(row=r, column=2).value = d["レアリティ"]
    ws.cell(row=r, column=4).value = d["在庫状況"]
    ws.cell(row=r, column=date_col).value = d["販売価格"]
    ws.cell(row=r, column=date_col+1).value = d["買取予想"]
    if date_col > 5:
        prev_price = ws.cell(row=r, column=date_col-4).value
        if prev_price and prev_price > 0 and d["販売価格"] > 0:
            ratio = round(d["販売価格"] / prev_price, 3)
            diff = d["販売価格"] - prev_price
            ws.cell(row=r, column=date_col+2).value = ratio
            ws.cell(row=r, column=date_col+3).value = diff

if "グラフ用" not in wb.sheetnames:
    wg = wb.create_sheet("グラフ用")
    wg["A1"] = "カード名を入力:"
    wg["B1"] = ""
    wg["A2"] = "開始日:"
    wg["B2"] = ""
    wg["A3"] = "終了日:"
    wg["B3"] = ""
    wg["A5"] = "日付"
    wg["B5"] = "販売価格"
    wg["C5"] = "買取予想"

wb.save(excel_path)
print("Excel保存完了！")

subprocess.run(["git", "config", "user.email", "bot@example.com"])
subprocess.run(["git", "co

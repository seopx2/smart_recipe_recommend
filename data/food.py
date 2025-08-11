from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import re

def extract_unit(name):
    match = re.search(r'\d+(g|kg|ml|L|개|봉|팩|입|장)', name)
    return match.group() if match else '기타'

category_map = {
    "채소": 907,
    "과일_견과_쌀": 908,
    "수산_해산_건어물": 909,
    "정육_가공육_달걀": 910,
    "국" : 911,
    "면" : 913,
    "음료" : 914,
    "베이커리" : 915,
    "우유_두유" : "018001",
    "요거트_생크림" : "018002",
    "자연치즈" : "018003",
    "가공치즈" : "018004",
    "버터" : "018005",
}

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 창 없이 실행할 거면 주석 해제
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_results = []  # ✅ 전체 결과 저장용

for category_name, category_id in category_map.items():
    driver.get(f"https://www.kurly.com/categories/{category_id}")
    time.sleep(3)

    for _ in range(15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    cards = driver.find_elements(By.CSS_SELECTOR, 'a.css-8bebpy')

    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, 'span.e1c07x485').text.strip()

            try:
                price = card.find_element(By.CSS_SELECTOR, 'span.sales-price span.price-number').text.strip()
            except:
                price = card.find_element(By.CSS_SELECTOR, 'span.price-number').text.strip()

            price = int(price.replace(',', ''))
            unit = extract_unit(name)
            all_results.append([name, category_name, price, unit])
        except Exception:
            continue

    print(f"✅ {category_name} 수집 완료")

# ✅ 모든 카테고리 합쳐서 한 파일로 저장
with open('kurly_all_categories.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['이름', '카테고리', '가격', '단위'])
    writer.writerows(all_results)

print(f"\n✅ 전체 저장 완료: 총 {len(all_results)}개 품목")

driver.quit()

import pandas as pd
import re

# 1. 마켓컬리 파일 불러오기
kurly = pd.read_csv("kurly_all_categories.csv")

# 2. 정규화 함수
def normalize(text):
    if pd.isna(text): return ''
    text = text.lower()  # 소문자
    text = re.sub(r'\s+', '', text)  # 공백 제거
    text = re.sub(r'\d+(g|kg|ml|l|개|봉|팩|입|장)', '', text)  # 단위 제거
    return text

# 3. 정규이름 컬럼 추가 (매칭용)
kurly['정규이름'] = kurly['이름'].apply(normalize)

# 4. 전처리된 결과 저장
kurly.to_csv("kurly_cleaned.csv", index=False, encoding="utf-8-sig")

print("✅ 마켓컬리 전처리 완료: '정규이름' 포함한 'kurly_cleaned.csv' 저장됨!")

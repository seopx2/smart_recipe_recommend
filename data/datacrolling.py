import requests
from urllib.parse import quote
import re
import pandas as pd
import time
import numpy as np

# 🔐 API 인증 정보
client_id = "nqdqrCQz_NvPlOSu4zra"  # 네이버 API Client ID
client_secret = "GW4Iw0FNFV"  # 네이버 API Client Secret

# 🔍 검색 키워드와 카테고리 정의
keywords = {
    # 채소류
    "신선식품 국내산 양파": "채소",
    "신선식품 국내산 당근": "채소",
    "신선식품 국내산 감자": "채소",
    "신선식품 국내산 대파": "채소",
    "신선식품 국내산 마늘": "채소",
    "신선식품 국내산 생강": "채소",
    "신선식품 국내산 청양고추": "채소",
    "신선식품 국내산 고추": "채소",
    "신선식품 국내산 애호박": "채소",
    "신선식품 국내산 오이": "채소",
    "신선식품 국내산 상추": "채소",
    "신선식품 국내산 깻잎": "채소",
    "신선식품 국내산 쑥갓": "채소",
    "신선식품 국내산 시금치": "채소",
    "신선식품 국내산 부추": "채소",
    "신선식품 국내산 미나리": "채소",
    "신선식품 국내산 쪽파": "채소",
    "신선식품 국내산 고구마": "채소",
    "신선식품 국내산 단호박": "채소",
    "신선식품 국내산 연근": "채소",
    "신선식품 국내산 우엉": "채소",
    "신선식품 국내산 무": "채소",
    "신선식품 국내산 배추": "채소",
    "신선식품 국내산 양배추": "채소",
    "신선식품 국내산 브로콜리": "채소",
    "신선식품 국내산 콜리플라워": "채소",
    "신선식품 국내산 아스파라거스": "채소",
    "신선식품 국내산 샐러리": "채소",
    "신선식품 국내산 파프리카": "채소",
    "신선식품 국내산 피망": "채소",
    
    # 육류
    "신선식품 국내산 돼지고기 목살": "육류",
    "신선식품 국내산 돼지고기 삼겹살": "육류",
    "신선식품 국내산 돼지고기 앞다리": "육류",
    "신선식품 국내산 돼지고기 뒷다리": "육류",
    "신선식품 국내산 돼지고기 갈비": "육류",
    "신선식품 국내산 소고기 등심": "육류",
    "신선식품 국내산 소고기 안심": "육류",
    "신선식품 국내산 소고기 갈비": "육류",
    "신선식품 국내산 소고기 양지": "육류",
    "신선식품 국내산 닭고기 가슴살": "육류",
    "신선식품 국내산 닭고기 다리": "육류",
    "신선식품 국내산 닭고기 날개": "육류",
    "신선식품 국내산 돼지고기" : "육류",
    "신선식품 국내산 소고기" : "육류",
    "신선식품 국내산 닭고기" : "육류",
    
    # 해산물
    "신선식품 국내산 고등어": "해산물",
    "신선식품 국내산 갈치": "해산물",
    "신선식품 국내산 삼치": "해산물",
    "신선식품 국내산 꽁치": "해산물",
    "신선식품 국내산 연어": "해산물",
    "신선식품 국내산 새우": "해산물",
    "신선식품 국내산 오징어": "해산물",
    "신선식품 국내산 문어": "해산물",
    "신선식품 국내산 낙지": "해산물",
    "신선식품 국내산 홍합": "해산물",
    "신선식품 국내산 바지락": "해산물",
    "신선식품 국내산 조개": "해산물",
    
    # 양념류
    "전통 고추장": "양념",
    "전통 된장": "양념",
    "전통 간장": "양념",
    "국내산 고춧가루": "양념",
    "국내산 들기름": "양념",
    "국내산 참기름": "양념",
    "식용유": "양념",
    "엑스트라버진 올리브유": "양념",
    "천일염": "양념",
    "설탕": "양념",
    "후추": "양념",
    "카레가루": "양념",
    "마요네즈": "양념",
    "케찹": "양념",
    "머스타드": "양념",
    "와사비": "양념",
    "식초": "양념",
    "미림": "양념",
    "맛술": "양념",
    
    # 곡물/면류
    "국내산 쌀": "곡물",
    "국내산 찹쌀": "곡물",
    "국내산 보리": "곡물",
    "국내산 현미": "곡물",
    "국내산 스파게티면": "면류",
    "국내산 소면": "면류",
    "국내산 우동면": "면류",
    "국내산 칼국수면": "면류",
    "국내산 냉면": "면류",
    "국내산 당면": "면류",
    
    # 유제품
    "국내산 우유": "유제품",
    "국내산 요구르트": "유제품",
    "국내산 버터": "유제품",
    "국내산 치즈": "유제품",
    "국내산 생크림": "유제품",
    "국내산 요거트": "유제품",
    
    # 기타
    "국내산 계란": "기타",
    "국내산 두부": "기타",
    "국내산 콩나물": "기타",
    "국내산 숙주나물": "기타",
    "국내산 시금치": "기타",
    "국내산 김치": "기타",
    "국내산 깨": "기타",
    "국내산 잣": "기타",
    "국내산 땅콩": "기타",
    "국내산 아몬드": "기타",
    "국내산 호두": "기타",
    "국내산 밤": "기타",
    "국내산 대추": "기타",
    "국내산 건포도": "기타",
    "국내산 말린 표고버섯": "기타",
    "국내산 말린 미역": "기타",
    "국내산 말린 다시마": "기타",
    "국내산 말린 멸치": "기타",
    "국내산 말린 새우": "기타",
    "국내산 말린 오징어": "기타"
}

# 📦 결과 저장 리스트
result = []

# 🔁 각 키워드에 대해 API 호출
for query, category in keywords.items():
    try:
        url = f"https://openapi.naver.com/v1/search/shop.json?query={quote(query)}&display=30&start=1&sort=asc"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()  # HTTP 오류 체크
        data = res.json()

        # ✅ 가격 정보 수집
        items = data.get("items", [])
        
        # 가공식품, 도구 등 제외하고 순수 식재료만 필터링
        fresh_items = []
        for item in items:
            title = item['title'].lower()
            
            # 제외할 키워드들 (확장)
            exclude_keywords = [
                # 가공식품 관련
                '요구르트', '주스', '즙', '가루', '분말', '건조', '절임', '피클', '통조림', '냉동', '냉장',
                '세트', '선물세트', '기프트', '선물용', '선물', '패키지', '구성', '세트상품',
                # 도구/기구 관련
                '망', '볼', '슬라이서', '칼', '도구', '기구', '세트', '컵', '접시', '그릇', '보관용기',
                '포크', '젓가락', '수저', '냄비', '프라이팬', '조리도구', '조리기구',
                # 가공/조리 관련
                '조리', '가공', '제조', '생산', '제작', '만들기', '레시피', '조리법',
                # 기타
                '다이어트', '건강', '영양제', '보조식품', '기능성', '건강기능식품'
            ]
            
            # 필수 포함 키워드 (식재료 특성)
            required_keywords = [
                '신선', '생', '냉장', '냉동', '냉장보관', '냉동보관',
                '국내산', '국산', '제철', '당일', '직송', '산지직송'
            ]
            
            # 검색하려는 식재료명
            ingredient_name = query.split()[-1]
            
            # 카테고리 확인
            categories = [item.get(f"category{i}", "") for i in range(1, 5)]
            is_food_category = any('식품' in cat for cat in categories)
            
            # 필터링 조건
            has_excluded_keywords = any(x in title for x in exclude_keywords)
            has_required_keywords = any(x in title for x in required_keywords)
            has_ingredient = ingredient_name in title
            
            # 제외 키워드가 없고, 필수 키워드가 있으며, 식재료명이 포함되어 있고, 식품 카테고리인 경우만 선택
            if not has_excluded_keywords and has_required_keywords and has_ingredient and is_food_category:
                fresh_items.append(item)
        
        items = fresh_items
        prices = [int(item["lprice"]) for item in items]
        
        if prices:
            # 최저가 상품 찾기
            lowest_item = min(items, key=lambda x: int(x["lprice"]))
            
            title = re.sub(r'<[^>]+>', '', lowest_item['title'])  # HTML 태그 제거
            price = int(lowest_item['lprice'])
            full_category = " > ".join(filter(None, [lowest_item.get(f"category{i}") for i in range(1, 5)]))

            # 📏 단위 추출
            unit_match = re.search(r'(\d+\.?\d*)\s*(kg|g|봉|팩|개|병|통|박스)', title.lower())
            unit = unit_match.group(0) if unit_match else "정보 없음"

            result.append({
                "식재료명": title,
                "카테고리": category,
                "세부 카테고리": full_category,
                "가격": price,
                "단위": unit
            })

            print(f"{query} 검색 완료: 최저가 {price}원")
        else:
            print(f"{query}에 대한 검색 결과가 없습니다.")

        time.sleep(0.5)  # 호출 제한 방지용 대기

    except Exception as e:
        print(f"{query} 검색 중 오류 발생: {str(e)}")
        continue

# 💾 CSV로 저장
if result:
    try:
        # 기존 파일이 있는지 확인
        try:
            existing_df = pd.read_csv("장보기_리스트.csv", encoding='utf-8-sig')
            if not existing_df.empty:
                new_df = pd.DataFrame(result)
                # 기존 데이터와 새로운 데이터 합치기
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                combined_df.to_csv("장보기_리스트.csv", index=False, encoding='utf-8-sig')
                print(f"\n총 {len(result)}개의 상품이 기존 장보기_리스트.csv 파일에 추가되었습니다.")
            else:
                # 파일이 비어있는 경우
                df = pd.DataFrame(result)
                df.to_csv("장보기_리스트.csv", index=False, encoding='utf-8-sig')
                print(f"\n총 {len(result)}개의 상품이 장보기_리스트.csv 파일에 저장되었습니다.")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # 파일이 없거나 비어있는 경우 새로 생성
            df = pd.DataFrame(result)
            df.to_csv("장보기_리스트.csv", index=False, encoding='utf-8-sig')
            print(f"\n총 {len(result)}개의 상품이 장보기_리스트.csv 파일에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {str(e)}")
else:
    print("저장할 상품이 없습니다.")

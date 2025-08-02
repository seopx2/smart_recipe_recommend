import requests, json
from bs4 import BeautifulSoup
import csv
def food_info(name):
    url = f"https://www.10000recipe.com/recipe/list.html?q={name}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("HTTP response error:", response.status_code)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    food_list = soup.find_all(attrs={'class': 'common_sp_link'})
    if not food_list:
        print(f"[X] '{name}' 검색 결과 없음")
        return None

    food_id = food_list[0]['href'].split('/')[-1]
    new_url = f'https://www.10000recipe.com/recipe/{food_id}'
    new_response = requests.get(new_url, headers=headers)
    if new_response.status_code != 200:
        print("HTTP response error:", new_response.status_code)
        return None

    soup = BeautifulSoup(new_response.text, 'html.parser')
    food_info_tag = soup.find(attrs={'type': 'application/ld+json'})
    if not food_info_tag:
        print(f"[X] '{name}' 레시피 정보 없음")
        return None

    result = json.loads(food_info_tag.text)

    # 재료 처리
    ingredient = ', '.join(result.get('recipeIngredient', []))

    # 레시피 단계가 없는 경우 예외 처리
    if 'recipeInstructions' not in result:
        print(f"[X] '{name}' 레시피 단계 없음")
        return None

    # 정상적으로 레시피 구성
    recipe = [f"{i+1}. {step['text']}" for i, step in enumerate(result['recipeInstructions'])]

    return {
        'name': name,
        'ingredients': ingredient,
        'recipe': recipe
    }
# 음식 카테고리별 리스트
korean_foods = [
    "김치찌개", "된장찌개", "불고기", "비빔밥", "갈비찜", "잡채", "삼계탕", "떡볶이", "순두부찌개", "제육볶음",
    "파전", "감자탕", "오징어볶음", "닭갈비", "콩나물국", "부대찌개", "갈비탕", "해물파전", "수육", "동태찌개"
]
japanese_foods = [
    "스시", "라멘", "우동", "규동", "가츠동", "오코노미야키", "타코야키", "덴푸라", "야키소바", "돈카츠",
    "가라아게", "스키야키", "샤브샤브", "오야코동", "니쿠자가", "야키토리", "미소시루", "에비후라이", "카레우동", "모츠나베"
]
chinese_foods = [
    "짜장면", "짬뽕", "탕수육", "마파두부", "깐풍기", "유산슬", "팔보채", "양장피", "고추잡채", "깐쇼새우",
    "동파육", "훠궈", "꿔바로우", "라조기", "멘보샤", "마라탕", "마라샹궈", "춘권", "어향육슬", "고량주"
]
western_foods = [
    "스테이크", "파스타", "피자", "리조또", "샐러드", "라자냐", "감바스", "카프레제", "크림스프", "치킨스테이크",
    "미트볼", "프렌치토스트", "오믈렛", "클럽샌드위치", "치즈오븐스파게티", "감자그라탕", "바질페스토파스타", "치킨파르메산", "에그베네딕트", "로스트치킨"
]
side_dishes = [
    "계란말이", "멸치볶음", "시금치나물", "감자조림", "콩자반", "오이무침", "진미채볶음", "애호박볶음", "두부조림", "무생채",
    "고등어조림", "연근조림", "미역줄기볶음", "마늘쫑볶음", "버섯볶음", "깻잎장아찌", "파래무침", "가지볶음", "어묵볶음", "브로콜리나물"
]
diet_foods = [
    "닭가슴살샐러드", "두부샐러드", "오트밀죽", "현미밥", "닭가슴살스테이크", "연어샐러드", "곤약볶음밥", "채소스틱", "아보카도샐러드", "닭가슴살구이",
    "두부스테이크", "샐러드랩", "병아리콩샐러드", "닭가슴살샌드위치", "고구마샐러드", "채소볶음밥", "닭가슴살월남쌈", "그릭요거트볼", "닭가슴살카레", "채소스무디"
]
fusion_foods = [
    "김치볶음밥피자", "불고기파스타", "떡갈비버거", "고추장파스타", "치즈떡볶이피자", "불닭크림파스타", "김치나베", "된장파스타", "불고기타코", "김치치즈스파게티",
    "매운치킨퀘사디아", "불고기피자", "고구마피자", "김치라자냐", "불닭리조또", "된장리조또", "불고기샌드위치", "김치치즈오믈렛", "불닭파니니", "고추장리조또"
]
dessert_foods = [
    "티라미수", "치즈케이크", "브라우니", "마카롱", "푸딩", "에그타르트", "크렘브륄레", "초코칩쿠키", "딸기케이크", "롤케이크",
    "바나나빵", "팬케이크", "와플", "젤라또", "수플레", "파블로바", "레몬타르트", "카라멜푸딩", "오레오케이크", "초코무스"
]

# 카테고리별로 크롤링 및 출력
categories = [
    ("한식", korean_foods),
    ("일식", japanese_foods),
    ("중식", chinese_foods),
    ("양식", western_foods),
    ("반찬류", side_dishes),
    ("건강식/다이어트", diet_foods),
    ("퓨전류", fusion_foods),
    ("디저트류", dessert_foods)
]

# CSV 파일 저장
with open("recipes.csv", mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["카테고리", "메뉴", "재료", "레시피"])  # 헤더

    for category, food_list in categories:
        print(f"\n===== {category} =====")
        for name in food_list:
            result = food_info(name)
            if result:
                print(f"\n메뉴: {result['name']}")
                print(f"재료: {result['ingredients']}")
                print("레시피:")
                for step in result['recipe']:
                    print(step)

                recipe_text = "\n".join(result['recipe'])
                writer.writerow([category, result['name'], result['ingredients'], recipe_text])

print("\n✅ recipes.csv 파일로 저장 완료!")

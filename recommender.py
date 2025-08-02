import pandas as pd
import os
import re
from sentence_transformers import SentenceTransformer, util
from utils import normalize  # normalize 함수는 텍스트 전처리 용도 (소문자, 공백 제거 등)

# 상대 경로 설정
base_dir = os.path.dirname(__file__)
recipes_path = os.path.join(base_dir, "data/recipes.csv")
kurly_path = os.path.join(base_dir, "data/kurly.csv")

# 데이터 불러오기
recipes = pd.read_csv(recipes_path)
kurly = pd.read_csv(kurly_path)

# SBERT 모델 로딩 (국문 전용)
model = SentenceTransformer('jhgan/ko-sbert-nli')

def recommend_recipes(user_ingredients):
    user_ingredients = [normalize(i) for i in user_ingredients]
    user_embeds = model.encode(user_ingredients, convert_to_tensor=True)

    results = []

    for _, row in recipes.iterrows():
        recipe_ings = [normalize(i) for i in row["재료"].split(",")]
        have = []
        need = []
        total_cost = 0

        for ing in recipe_ings:
            ing_embed = model.encode(ing, convert_to_tensor=True)
            cosine_scores = util.cos_sim(ing_embed, user_embeds)
            max_score = cosine_scores.max().item()

            if max_score > 0.7:  # ✅ 임계값 조절 가능
                have.append(ing)
            else:
                need.append(ing)

        if not have:
            continue

        match_score = len(have) / len(recipe_ings)

        # 부족한 재료를 마켓컬리 데이터와 매칭
        items = []
        for ing in need:
            match = kurly[kurly['정규이름'].str.contains(ing, na=False)]
            for _, r in match.head(2).iterrows():
                items.append({
                    "재료명": ing,
                    "이름": r["이름"],
                    "가격": r["가격"],
                    "단위": r["단위"]
                })
                total_cost += r["가격"]

        results.append({
            "메뉴": row['메뉴'],
            "매칭률": round(match_score, 2),
            "부족재료": list(need),
            "레시피": row['레시피'],
            "추천상품": items
        })

    return sorted(results, key=lambda x: x['매칭률'], reverse=True)[:5]


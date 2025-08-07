from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import List

from recommender import recommend_recipes
import csv
import os
import re

#if __name__ == "__main__":
#    import uvicorn
#    import os

#    port = int(os.environ.get("PORT", 8000))  # Render가 지정한 포트를 가져옴
#    uvicorn.run("main:app", host="0.0.0.0", port=port)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#추천결과 저장
recommendation_cache = []

#시작 페이지
@app.get("/")
async def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

#재료 입력
class IngredientInput(BaseModel):
    ingredients: List[str]

#캐싱 추가
@app.post("/recommend") 
def get_recommendations(input: IngredientInput):
    results = recommend_recipes(input.ingredients)
    global recommendation_cache
    recommendation_cache = results  #전역 변수에 저장
    return {"recommendations": results}


#추천 결과 API
@app.post("/recommend") 
def get_recommendations(input: IngredientInput):
    results = recommend_recipes(input.ingredients)
    return {"recommendations": results}

#추천 결과 페이지 1
@app.get("/result")
def result_page(request: Request):
    return templates.TemplateResponse("index_results.html", {"request": request})

#추천 결과 페이지 2
def get_recipe_by_id(recipe_id: str):
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data/recipes.csv")

    try:
        recipe_id = int(recipe_id)
    except ValueError:
        return None

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))  # list로 감싸기

        if 0 <= recipe_id < len(reader):
            recipe = reader[recipe_id]
            if recipe.get('레시피'):
                lines = recipe['레시피'].split('\n')
                cleaned_lines = [re.sub(r'^\d+\.\s*', '', line) for line in lines]
                recipe['레시피'] = '\n'.join(cleaned_lines)

            return recipe
        else:
            return None

#상세 페이지
@app.get("/detail", response_class=HTMLResponse)
async def recipe_detail(request: Request, id: str):
    recipe = get_recipe_by_id(id)
    if recipe is None:
        return templates.TemplateResponse("404.html", {"request": request})

    #최근 추천 결과에서 해당 ID에 맞는 레시피 정보 가져오기
    try:
        recipe_index = int(id)
    except ValueError:
        return templates.TemplateResponse("404.html", {"request": request})

    if recipe_index >= len(recommendation_cache):
        return templates.TemplateResponse("404.html", {"request": request})

    match_info = recommendation_cache[recipe_index]

    return templates.TemplateResponse("details.html", {
        "request": request,
        "recipe": recipe,
        "name" : match_info.get("메뉴"),
        "matching_rate": match_info.get("매칭률"),
        "missing_ingredients": match_info.get("부족재료"),
        "recommended_items": match_info.get("추천상품")
    })

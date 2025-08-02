from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from recommender import recommend_recipes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flutter 웹 앱 주소만 넣고 싶으면 여기에 정확히 써도 됨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngredientInput(BaseModel):
    ingredients: List[str]

@app.post("/recommend")
def get_recommendations(input: IngredientInput):
    results = recommend_recipes(input.ingredients)
    return {"recommendations": results}

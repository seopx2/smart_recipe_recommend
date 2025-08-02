from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from pydantic import BaseModel
from typing import List
from recommender import recommend_recipes


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flutter 웹 앱 주소만 넣고 싶으면 여기에 정확히 써도 됨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

class IngredientInput(BaseModel):
    ingredients: List[str]

@app.post("/recommend")
def get_recommendations(input: IngredientInput):
    results = recommend_recipes(input.ingredients)
    return {"recommendations": results}

@app.get("/result")
def result_page(request: Request):
    return templates.TemplateResponse("index_results.html", {"request": request})


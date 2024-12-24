import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import os

app = FastAPI()

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")

# Файл для хранения данных об играх
GAMES_FILE = "games.json"

def get_psn_games():
    url = "https://store.playstation.com/en-us/pages/deals"

    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        games = []
        for item in soup.select('.discount-item-selector'): 
            title = item.select_one('.title-selector').text.strip() 
            price = item.select_one('.price-selector').text.strip()
            link = item.select_one('a')['href']  
            image = item.select_one('img')['src'] if item.select_one('img') else None  
            
            games.append({
                'title': title,
                'price': price,
                'link': link,
                'image': image
            })

        # Проверяем, есть ли игры перед сохранением
        if games:
            with open(GAMES_FILE, 'w') as f:
                json.dump(games, f)
        else:
            print("Нет доступных игр для сохранения.")

        return games
    except Exception as e:
        print(f"Error fetching games: {e}")
        return []

@app.get("/")
async def root(request: Request):
    games = get_psn_games()  
    return templates.TemplateResponse("index.html", {"request": request, "games": games})

@app.get("/games")
async def read_games(search: str = Query(None)):
    if os.path.exists(GAMES_FILE):
        with open(GAMES_FILE, 'r') as f:
            try:
                games = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON. Файл может быть пустым или поврежденным.")
                games = []
    else:
        games = get_psn_games()  

    if search:
        games = [game for game in games if search.lower() in game['title'].lower()]

    return JSONResponse(content=games)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

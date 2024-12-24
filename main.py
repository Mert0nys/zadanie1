from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import telebot
import json

app = FastAPI()
bot = telebot.TeleBot('7861739670:AAGJpkw0lseuOJBkwQfpp4XuBQxpeiXKiVQ')

# Загрузка данных из JSON
with open('games.json', 'r') as f:
    games = json.load(f)

@app.get("/")
async def root():
    return {"message": "Welcome to PSN Store Telegram Mini App!"}

@app.get("/games", response_class=HTMLResponse)
async def get_games(discount_threshold: int = 0):
    filtered_games = [game for game in games if int(game['discount_percentage'].replace('%', '')) >= discount_threshold]
    
    html_content = "<h1>Список игр со скидками</h1><ul>"
    for game in filtered_games:
        html_content += f"<li>{game['title']} - {game['current_price']} (Старая цена: {game['old_price']}, Скидка: {game['discount_percentage']}) - <a href='{game['link']}'>Подробнее</a></li>"
    html_content += "</ul>"
    
    return HTMLResponse(content=html_content)

# Обработчик команд Telegram
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Используйте команду /games для получения списка игр со скидками.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

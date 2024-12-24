import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_psn_store():
    url = "https://store.playstation.com/en-tr/home/games"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    games = []
    
    # Примерный селектор для извлечения данных (может потребоваться корректировка)
    for game in soup.select('.some-game-selector'):
        title = game.select_one('.game-title-selector').text.strip()
        current_price = game.select_one('.current-price-selector').text.strip()
        old_price = game.select_one('.old-price-selector').text.strip()
        discount_percentage = game.select_one('.discount-percentage-selector').text.strip()
        end_date = game.select_one('.end-date-selector').text.strip()

        games.append({
            'title': title,
            'current_price': current_price,
            'old_price': old_price,
            'discount_percentage': discount_percentage,
            'end_date': end_date,
            'link': game.select_one('a')['href']  # Ссылка на игру
        })

    return games

def save_to_json(games, filename='games.json'):
    with open(filename, 'w') as f:
        json.dump(games, f)

def save_to_csv(games, filename='games.csv'):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=games[0].keys())
        writer.writeheader()
        writer.writerows(games)

if __name__ == "__main__":
    games = parse_psn_store()
    save_to_json(games)
    save_to_csv(games)

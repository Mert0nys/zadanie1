import telebot
from main import get_psn_discounts


API_TOKEN = '7861739670:AAGJpkw0lseuOJBkwQfpp4XuBQxpeiXKiVQ' 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который уведомляет о скидках на PSN. Используйте /discounts, чтобы получить информацию о скидках.")

@bot.message_handler(commands=['discounts'])
def send_discounts(message):
    try:
        discounts = get_psn_discounts()
        if discounts:
            response = "\n".join([f"{item['title']}: {item['price']}" for item in discounts])
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Нет доступных скидок.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":

    bot.polling()
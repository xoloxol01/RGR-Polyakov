import telebot

bot = telebot.TeleBot('6778234952:AAEA3S8J-k5XU1LIliq-fKrZajQTuSSBAeo')

@bot.message_handler(commands=['start'])
def main(message): #хранение информации для чата
    bot.send_message(message.chat.id, 'Привет!')

bot.polling(none_stop=True) #бесконечный цикл

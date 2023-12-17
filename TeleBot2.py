import telebot
from telebot import types

bot = telebot.TeleBot('6778234952:AAEA3S8J-k5XU1LIliq-fKrZajQTuSSBAeo')

# Хранилище информации о счетах и активах для каждого пользователя
user_accounts = {}
user_assets = {}
current_account = {}

# Функция для главного меню
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Создать новый брокерский счет', 'Просмотреть существующие', 'Изменить брокерский счет') 
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Функция для меню управления счетом
def account_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Добавить актив', 'Удалить счет', 'Вернуться в главное меню')
    bot.send_message(message.chat.id, "Выберите действие для счета:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def welcome(message):
    user_accounts[message.chat.id] = []
    user_assets[message.chat.id] = {}
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      'Я - ваш личный бот по управлению инвестициями. '
                                      'Создавайте брокерские счета, добавляйте активы и отслеживайте свои инвестиции.\n'
                                      'Используйте команды или меню для навигации.')
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Создать новый брокерский счет")
def request_account_name(message):
    msg = bot.send_message(message.chat.id, "Введите название для нового брокерского счета:")
    bot.register_next_step_handler(msg, create_account)

def create_account(message):
    account_name = message.text
    user_accounts[message.chat.id].append(account_name)
    user_assets[message.chat.id][account_name] = []
    current_account[message.chat.id] = account_name
    bot.send_message(message.chat.id, f"Брокерский счет '{account_name}' создан.")
    account_menu(message)

@bot.message_handler(func=lambda message: message.text == "Добавить актив")
def add_asset_type(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Акции', 'Облигации')
    msg = bot.send_message(message.chat.id, "Выберите тип актива:", reply_markup=markup)
    bot.register_next_step_handler(msg, add_asset)

def add_asset(message):
    asset_type = message.text
    msg = bot.send_message(message.chat.id, f"Введите название и количество {asset_type}, разделенные запятой (например, 'Apple, 10'):")
    bot.register_next_step_handler(msg, add_asset_details, asset_type)

def add_asset_details(message, asset_type):
    try:
        name, quantity = message.text.split(', ')
        quantity = int(quantity)
        account = current_account.get(message.chat.id)
        user_assets[message.chat.id][account].append({'type': asset_type, 'name': name, 'quantity': quantity})
        bot.send_message(message.chat.id, f"Актив {name} ({quantity} шт.) добавлен в счет '{account}'.")
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка в формате данных. Попробуйте еще раз.")
    account_menu(message)

@bot.message_handler(func=lambda message: message.text == "Удалить счет")
def delete_account_step(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(message.chat.id, "Вы уверены, что хотите удалить текущий счет? (Да/Нет)", reply_markup=markup)
    bot.register_next_step_handler(msg, confirm_delete_account)

def confirm_delete_account(message):
    if message.text.lower() == 'да':
        account_name = current_account[message.chat.id]
        user_accounts[message.chat.id].remove(account_name)
        del user_assets[message.chat.id][account_name]
        bot.send_message(message.chat.id, f"Брокерский счет '{account_name}' удален.")
        main_menu(message)
    elif message.text.lower() == 'нет':
        edit_account(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите 'Да' или 'Нет'.")
        delete_account_step(message)


@bot.message_handler(func=lambda message: message.text == "Просмотреть существующие")
def view_accounts(message):
    if user_accounts[message.chat.id]:
        response = "Ваши счета:\n"
        for account in user_accounts[message.chat.id]:
            response += f"\n{account}:\n"
            for asset in user_assets[message.chat.id][account]:
                response += f"  - {asset['type']}: {asset['name']} (Количество: {asset['quantity']})\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас пока нет брокерских счетов.")
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Изменить брокерский счет")
def change_account_step(message):
    if user_accounts[message.chat.id]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for account in user_accounts[message.chat.id]:
            markup.add(account)
        msg = bot.send_message(message.chat.id, "Выберите счет для изменения:", reply_markup=markup)
        bot.register_next_step_handler(msg, edit_account)
    else:
        bot.send_message(message.chat.id, "У вас пока нет брокерских счетов.")
        main_menu(message)

def edit_account(message):
    account_name = message.text
    if account_name in user_accounts[message.chat.id]:
        current_account[message.chat.id] = account_name
        bot.send_message(message.chat.id, f"Вы выбрали счет '{account_name}'. Что вы хотите изменить?", reply_markup=edit_account_markup())
    else:
        bot.send_message(message.chat.id, "Такого счета не существует.")
        main_menu(message)

def edit_account_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Добавить актив', 'Удалить актив', 'Изменить название счета', 'Вернуться в главное меню')
    return markup

@bot.message_handler(func=lambda message: message.text == "Изменить название счета")
def change_account_name_step(message):
    msg = bot.send_message(message.chat.id, "Введите новое название для счета:")
    bot.register_next_step_handler(msg, change_account_name)

def change_account_name(message):
    new_account_name = message.text
    user_accounts[message.chat.id].remove(current_account[message.chat.id])
    user_accounts[message.chat.id].append(new_account_name)
    user_assets[message.chat.id][new_account_name] = user_assets[message.chat.id].pop(current_account[message.chat.id])
    current_account[message.chat.id] = new_account_name
    bot.send_message(message.chat.id, f"Название счета изменено на '{new_account_name}'.")
    edit_account(message)

@bot.message_handler(func=lambda message: message.text == "Вернуться в главное меню")
def return_to_main_menu(message):
    main_menu(message)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>мне</b> <u>бы</u> кто помог!', parse_mode='html')

bot.polling(none_stop=True)

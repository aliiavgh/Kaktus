
import telebot
from MyToken import token
from   telebot import types
import csv
import pandas as pd
from main import main

bot = telebot.TeleBot(token)

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('News today', callback_data='income')
exit = types.InlineKeyboardButton('Quit', callback_data='quit')
inline_keyboard.add(btn1, exit)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Show the news for today?', reply_markup=inline_keyboard)
main()

def list_news():
    with open('titles.txt', 'r') as file: 
        reader = file.readlines()
        n = [f'{reader.index(l_item)} {l_item}' for l_item in reader[0:20]]
        news = []
        for item in n:
            item_ = item.replace('\n', '')
            news.append(item_)
        return news
        


@bot.callback_query_handler(func = lambda c: True)
def inline(call): #message
    if call.data == 'income':
        chat_id = call.message.chat.id
        all_news = list_news()
        bot.send_message(chat_id, 'Enter a number')
        for i in range(21):
            bot.send_message(chat_id, all_news[i])
        
        # bot.send_message(chat_id, f'Latest news: \n{all_news}')

    if call.data == 'quit':
        chat_id = call.message.chat.id
        bot.send_message(chat_id, 'До свидания!')

choice = []

@bot.message_handler(commands=['Description'])
def descripption(message):
    data = pd.read_csv('news.csv', sep=";", error_bad_lines=False)
    try:
        global choice
        chat_id = message.chat.id
        time = data.iloc[choice[0]-1, 0]
        bot.send_message(chat_id, time, reply_markup=inline_keyboard)
    except:
        bot.send_message(chat_id, 'Empty!', reply_markup=inline_keyboard)

@bot.message_handler(commands=['Photo'])
def descripption(message):
    data = pd.read_csv('news.csv', sep=";", error_bad_lines=False)
    try:
        global choice
        chat_id = message.chat.id
        image = data.iloc[choice[0]-1, 2]
        bot.send_message(chat_id, image, reply_markup=inline_keyboard)
    except:
        bot.send_message(chat_id, 'Empty!', reply_markup=inline_keyboard)

@bot.message_handler(content_types=['text'])
def item(message): 
    global choice
    choice *= 0
    chat_id = message.chat.id
    j = int(message.text)
    choice.append(j)
    income_keyboard = types.ReplyKeyboardMarkup()
    description = types.InlineKeyboardButton('/Description', callback_data='descr')
    image = types.InlineKeyboardButton('/Photo', callback_data='photo')
    income_keyboard.add(description, image)
    try: 
        if j in range(22):
            with open('titles.txt') as file:
                reader = file.readlines()
                item = list(reader)[j]
                response = f'The news item №{reader.index(item)}: {item}'
                bot.send_message(chat_id, 'some title news you can see Description of this news and Photo', reply_markup=income_keyboard)
                bot.send_message(chat_id, response)
    
    except: 
        bot.send_message(chat_id, 'There is no such news!')


if __name__ == '__main__':
    bot.infinity_polling()
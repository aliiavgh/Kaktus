
import telebot
from MyToken import token
from   telebot import types
from parsing_k_m import *

bot = telebot.TeleBot(token)

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('News today', callback_data='income')
exit = types.InlineKeyboardButton('Quit', callback_data='quit')
inline_keyboard.add(btn1, exit)

income_keyboard = types.ReplyKeyboardMarkup()
btn2 = types.InlineKeyboardButton('Description', callback_data='descr')
income_keyboard.add(btn2)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Show the news for today?', reply_markup=inline_keyboard)


def list_news():
    with open('news.txt', 'r') as file: 
        
        reader = file.readlines()
        news = []
        for item in reader:
            item.replace('\n', '')
            news.append(item)
        news = list(enumerate(news))[0:21]
        return f'Новости сегодня: {news}'
        


@bot.callback_query_handler(func = lambda c: True)
def inline(call): #message
    if call.data == 'income':
        chat_id = call.message.chat.id
        list_news_ = list_news()
        bot.send_message(chat_id, list_news_)
        bot.send_message(chat_id, 'Enter a number')

    if call.data == 'quit':
        chat_id = call.message.chat.id
        bot.send_message(chat_id, 'До свидания!')

    

@bot.message_handler(content_types=['text'])
def item(message): 
    chat_id = message.chat.id
    j = int(message.text)
    try: 
        if j in range(20):
            with open('news.txt') as file:
                reader = file.readlines()
                item = list(reader)[j]
                bot.send_message(chat_id, 'some title news you can see Description of this news and Photo')
                bot.send_message(chat_id, item)

                with open('news.csv') as file:
                    reader1 = csv.reader(file)
                    bot.send_message(chat_id, list(reader1)[j], reply_markup=inline_keyboard)                
    except: 
        bot.send_message(chat_id, 'There is no such news!')


# @bot.callback_query_handler(func = lambda c: True)
# def income(c):
#     if c.data == 'descr':
#         chat_id = c.message.chat.id
#         global choice
#         with open('news.csv') as file:
#             reader = csv.reader(file)
#             bot.send_message(chat_id, list(reader)[choice[0]], reply_markup=inline_keyboard)

if __name__ == '__main__':
    bot.infinity_polling()
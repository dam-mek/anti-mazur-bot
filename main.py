import telebot
import texts
import os


bot = telebot.TeleBot(os.environ.get('TOKEN_AMB'))


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.chat.username)
    bot.send_message(message.chat.id, 'I did start')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


@bot.message_handler(content_types=['text'])
def dialogue(message):
    print(message.chat.username, message.text)
    if message.text.lower() in {'suck', 'пососи'}:
        bot.send_message(message.chat.id, texts.suck)
    elif message.text.lower() in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(message.chat.id, texts.cadillac)
    elif message.text.lower() in {'baby', 'малышка'}:
        bot.send_message(message.chat.id, texts.baby)
    elif message.text.lower().replace('ё', 'е') in {'ice', 'лед'}:
        bot.send_message(message.chat.id, texts.ice)
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')
    print(message)


@bot.message_handler(content_types=['sticker'])
def start_message(message):
    print(message)


bot.polling()

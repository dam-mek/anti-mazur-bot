from flask import Flask, request
import telebot
import texts
import os


server = Flask(__name__)
token = os.environ.get('TOKEN_AMB')
bot = telebot.TeleBot(token)


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
    elif message.text.lower().replace('ё', 'е') in {'ice', 'лед', 'айс'}:
        bot.send_message(message.chat.id, texts.ice)
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')
    print(message)


@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://anti-mazur.herokuapp.com/' + token)
    return "!", 200


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

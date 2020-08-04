from flask import Flask, request
import telebot
import texts
import os
import messages
import time
import markups


server = Flask(__name__)
token = os.environ.get('TOKEN_AMB')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    log(message)
    bot.send_message(message.chat.id, messages.HELLO, reply_markup=markups.source_markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    log(message)
    bot.send_message(message.chat.id, messages.HELP, reply_markup=markups.source_markup)


commands = {'/start': start_message, '/help': help_message}


@bot.message_handler(content_types=['text'])
def dialogue(message):
    log(message)

    if message.text.lower() in {'suck', 'пососи'}:
        bot.send_message(message.chat.id, texts.suck)
    elif message.text.lower() in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(message.chat.id, texts.cadillac)
    elif message.text.lower() in {'baby', 'малышка'}:
        bot.send_message(message.chat.id, texts.baby)
    elif message.text.lower() in {'ice', 'лед', 'лёд', 'айс'}:
        bot.send_message(message.chat.id, texts.ice)
    elif message.text.lower() == 'перевести текст в синонимы':
        msg = bot.send_message(message.chat.id, messages.ASK_TEXT)
        bot.register_next_step_handler(msg, ask_text)
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


def log(msg):
    date = msg.date
    date = '{}.{}.{} {}:{}:{}'.format(time.gmtime(date).tm_mday, time.gmtime(date).tm_mon, time.gmtime(date).tm_year,
                                      time.gmtime(date).tm_hour, time.gmtime(date).tm_min, time.gmtime(date).tm_sec)
    print('message id: ', msg.message_id, '\n',
          'date: ', date, '\n',
          'user id: ', msg.from_user.id, '\n',
          'username: ', msg.from_user.username, '\n',
          'first name: ', msg.from_user.first_name, '\n',
          'last name: ', msg.from_user.last_name, '\n',
          msg.text,
          sep='')


def ask_text(message):
    log(message)
    if message.text is None:
        msg = bot.send_message(message.chat.id, messages.ASK_EXACTLY_TEXT)
        bot.register_next_step_handler(msg, ask_text)
        return
    if message.text in commands:
        commands[message.text](message)
    elif message.text == '/help':
        help_message(message)
    elif message.text.lower() in {'suck', 'пососи'}:
        bot.send_message(message.chat.id, texts.suck)
    elif message.text.lower() in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(message.chat.id, texts.cadillac)
    elif message.text.lower() in {'baby', 'малышка'}:
        bot.send_message(message.chat.id, texts.baby)
    elif message.text.lower() in {'ice', 'лед', 'лёд', 'айс'}:
        bot.send_message(message.chat.id, texts.ice)
    else:
        bot.send_message(message.chat.id, message.text)


@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'Ну типа АнтиМазур запущен', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://anti-mazur.herokuapp.com/' + token)
    return 'Ну типа АнтиМазур запущен, а я нужен для вебхука', 200


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

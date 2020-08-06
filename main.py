from synonym import parserSynonym
from flask import Flask, request
import telebot
import texts
import os
import messages
import time
import markups

# TODO
#  1) Синонимы
#  2) Логирование

server = Flask(__name__)
token = os.environ.get('TOKEN_AMB')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    log(message)
    bot.send_message(chat_id=message.chat.id, text=messages.HELLO, reply_markup=markups.source_markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    log(message)
    # bot.answer_callback_query(text='fuck')
    bot.send_message(chat_id=message.chat.id, text=messages.HELP, reply_markup=markups.source_markup)


@bot.message_handler(content_types=['text'])
def dialogue(message):
    log(message)
    if do_prikol(message):
        return
    if message.text.lower() == 'перевести текст в синонимы':
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_TEXT, reply_markup=markups.none_markup)
        bot.register_next_step_handler(msg, ask_text)
    else:
        bot.send_sticker(chat_id=message.chat.id,
                         data='CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


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
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_EXACTLY_TEXT)
        bot.register_next_step_handler(msg, ask_text)
        return
    msg = bot.send_message(chat_id=message.chat.id, text='Сделано: 0%')
    generator_text = parserSynonym.main(message.text)
    text = next(generator_text)
    while type(text) is int:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text='Сделано: ' + str(text) + '%')
        text_tmp = next(generator_text)
        while text_tmp == text:
            text_tmp = next(generator_text)
        text = text_tmp
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    bot.send_message(chat_id=message.chat.id, text=text,
                     reply_markup=markups.source_markup)
    print(text)


def do_prikol(msg):
    """
    It will do prikol. Return True if prikol can exist

    :param msg: <class 'telebot.types.Message'>
    :return: bool
    """
    if msg.text.lower() in {'suck', 'пососи'}:
        bot.send_message(msg.chat.id, texts.suck)
    elif msg.text.lower() in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(msg.chat.id, texts.cadillac)
    elif msg.text.lower() in {'baby', 'малышка'}:
        bot.send_message(msg.chat.id, texts.baby)
    elif msg.text.lower() in {'ice', 'лед', 'лёд', 'айс'}:
        bot.send_message(msg.chat.id, texts.ice)
    else:
        return False
    return True


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

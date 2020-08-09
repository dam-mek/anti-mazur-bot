from flask import Flask, request
from os import environ
from time import gmtime, asctime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import telebot

from synonym import parserSynonym
import messages
import markups

# TODO
#  1) Синонимы (допилить чуть Engine)
#  2) Логирование (logging)
#  3) Приколы в messages.video
#  4) Залить на свой гит

server = Flask(__name__)
token = environ.get('TOKEN_AMB')
password = environ.get('PASSWORD_AMB')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    send_mail(message)
    with open('log.log', 'a') as file:
        file.write('INFO:START:' + create_log_str(message) + '\n')
    bot.send_message(chat_id=message.chat.id, text=messages.START, reply_markup=markups.source_markup,
                     parse_mode='markdown')
    # bot.send_sticker(chat_id=message.chat.id,
    # data='CAACAgIAAxkBAAM3Xx3eHjxLZMGi9GQCWRozmRovnAsAAh4DAAKNSjADcnw1sWQ7ES8aBA')


@bot.message_handler(commands=['help'])
def help_message(message):
    with open('log.log', 'a') as file:
        file.write('INFO:HELP:' + create_log_str(message) + '\n')
    bot.send_message(chat_id=message.chat.id, text=messages.HELP, reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['about'])
def about_message(message):
    with open('log.log', 'a') as file:
        file.write('INFO:ABOUT:' + create_log_str(message) + '\n')
    bot.send_message(chat_id=message.chat.id, text=messages.ABOUT, reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    with open('log.log', 'a') as file:
        file.write('INFO:FEED:' + create_log_str(message) + '\n')
    bot.send_message(chat_id=message.chat.id, text=messages.FEEDBACK, reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(commands=['log'])
def feedback_message(message):
    if message.from_user.username != 'dam_mek':
        bot.send_message(chat_id=message.chat.id, text='*Ты чо удумал?!*', reply_markup=markups.source_markup,
                         parse_mode='markdown')
        with open('log.log', 'a') as file:
            file.write('INFO:LOG:' + create_log_str(message) + '\n')
        return
    filename = 'log.log'
    with open(filename, 'r') as file:
        global password
        email = 'denisov_aa@gkl-kemerovo.ru'
        mail_account = smtplib.SMTP('smtp.gmail.com', 587)
        mail_account.starttls()
        mail_account.login(user=email, password=password)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = 'Logging AntiMazur bot!'
        f = MIMEText(file.read(), _subtype='plain')
        f.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(f)

        text_message = 'Логи за ' + asctime()
        msg.attach(MIMEText(text_message, 'plain'))
        mail_account.send_message(from_addr=email, to_addrs=msg['To'], msg=msg)
        mail_account.quit()
    with open(filename, 'w') as file:
        file.write('======== LOGGING FILE FOR SOMELOG ======\n')
    bot.send_message(chat_id=message.chat.id, text='Всё сделано, Мой Господин', reply_markup=markups.source_markup,
                     parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def dialogue(message):
    with open('log.log', 'a') as file:
        file.write('INFO:DIAL:' + create_log_str(message) + '\n')
    if do_prikol(message):
        return
    if message.text.lower() == 'перевести текст в синонимы':
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_TEXT, reply_markup=markups.none_markup,
                               parse_mode='markdown')
        bot.register_next_step_handler(msg, ask_text)
    else:
        help_message(message)


@bot.message_handler(content_types=['video_note'])
def video(message):
    with open('log.log', 'a') as file:
        file.write('INFO:VIDEO:' + create_log_str(message) + '\n')
    bot.send_message(chat_id=message.chat.id, text=messages.video, reply_markup=markups.source_markup,
                     parse_mode='markdown')


def ask_text(message):
    with open('log.log', 'a') as file:
        file.write('INFO:ASK:' + create_log_str(message) + '\n')
    if message.text is None:
        msg = bot.send_message(chat_id=message.chat.id, text=messages.ASK_EXACTLY_TEXT, parse_mode='markdown')
        bot.register_next_step_handler(msg, ask_text)
        return
    msg = bot.send_message(chat_id=message.chat.id, text='Сделано: *0%*', parse_mode='markdown')
    generator_text = parserSynonym.main(message.text)
    text = next(generator_text)
    while type(text) is int:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f'Сделано: *{text}%*',
                              parse_mode='markdown')
        text_tmp = next(generator_text)
        while text_tmp == text:
            text_tmp = next(generator_text)
        text = text_tmp
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    bot.send_message(chat_id=message.chat.id, text=text,
                     reply_markup=markups.source_markup)
    with open('log.log', 'a') as file:
        file.write(f'INFO:RESULT:MSG_ID-{message.message_id}:' + text + '\n')


def do_prikol(msg):
    """
    It will do prikol. Return True if prikol can exist

    :param msg: <class 'telebot.types.Message'>
    :return: bool
    """
    text = msg.text.lower()
    if text in {'suck', 'пососи'}:
        bot.send_message(msg.chat.id, messages.suck)
    elif text in {'кадиллак', 'кадилак', 'cadillac', 'cadilac'}:
        bot.send_message(msg.chat.id, messages.cadillac)
    elif text in {'baby', 'малышка'}:
        bot.send_message(msg.chat.id, messages.baby)
    elif text in {'ice', 'лед', 'лёд', 'айс'}:
        bot.send_message(msg.chat.id, messages.ice)
    elif text in {'плодотворная дебютная идея'}:
        bot.send_message(msg.chat.id, messages.ostap)
    else:
        return False
    return True


def send_mail(message):
    global password
    email = 'denisov_aa@gkl-kemerovo.ru'
    mail_account = smtplib.SMTP('smtp.gmail.com', 587)
    mail_account.starttls()
    mail_account.login(user=email, password=password)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Logging. ' + message.from_user.username + ' sent a message to the bot!'
    text_message = create_log_str(message)
    msg.attach(MIMEText(text_message, 'plain'))
    mail_account.send_message(from_addr=email, to_addrs=msg['To'], msg=msg)
    mail_account.quit()


def create_log_str(msg):
    date = msg.date
    date = '{}.{}.{} {}:{}:{}'.format(str(gmtime(date).tm_mday).rjust(2, '0'), str(gmtime(date).tm_mon).rjust(2, '0'),
                                      str(gmtime(date).tm_year).rjust(2, '0'), str(gmtime(date).tm_hour).rjust(2, '0'),
                                      str(gmtime(date).tm_min).rjust(2, '0'), str(gmtime(date).tm_sec).rjust(2, '0'))

    log_str = 'message_id:{}|date:{}|used_id:{}|username:{}|first_name:{}|last_name:{}|text:{}'.format(
        msg.message_id, date, msg.from_user.id, msg.from_user.username,
        msg.from_user.first_name, msg.from_user.last_name, msg.text
    )
    return log_str


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
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))

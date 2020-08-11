from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

email = 'denisov_aa@gkl-kemerovo.ru'
password = 'ilovegkl-kemerovo'
msg = MIMEMultipart()
message = 'фу, у тебя воняет'
msg['From'] = email
msg['To'] = 'kalachikov_lv@gkl-kemerovo.ru'
msg['Subject'] = 'Пук'
msg.attach(MIMEText(message, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
print('2')
server.starttls()
server.login(user=email, password=password)
print('1')
for i in range(50):
    print(i)
    server.send_message(from_addr=email, to_addrs=msg['To'], msg=msg)
server.quit()

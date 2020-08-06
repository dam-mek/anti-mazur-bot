# -*- coding: utf-8 -*-
from synonym import EngineSynonym, ExtraStaff


# TODO
#  1) проверять регист букв в слове: слова могут быть в прописном шрифте (ТЕКСТ), только первая бука (Текст),
#  никакая (текст)
#  2) преобразование в начальную форму с помощью сайта для начальным форм
#  3) если перед словом стоит хэштег #, то слово не учитывается (#пропусти)
#  4) работа с словоизменением через https://www.translate.ru/grammar/ru-en/
#  5) создание телеграм-бота
#  6) личная база данных с синонимами
#  7) научиться работать с git


def convert_string2list(s):
    converted = []
    alpha = False
    for x in s:
        if x.isalpha() or x == '-':
            if alpha:
                converted[-1] += x
            else:
                converted.append(x)
            alpha = True
        else:
            if alpha or not converted:
                converted.append(x)
            else:
                converted[-1] += x
            alpha = False
    return converted


app = EngineSynonym.SynonymOnline()
app.add_site('https://synonymonline.ru', ExtraStaff.post0, ExtraStaff.convert_link0)
app.add_site('https://sinonim.org', ExtraStaff.post1, ExtraStaff.convert_link1)


def main(text):
    new_text = ''
    list_text = convert_string2list(text)
    for i in range(len(list_text)):
        symbols = list_text[i]
        if symbols.isalpha() and len(symbols) > 2:
            # print(symbols)
            syn = app.get(symbols)
            if symbols.isupper():
                syn = syn.upper()
            elif symbols.istitle():
                syn = syn.capitalize()
            elif symbols.islower():
                syn = syn.lower()
            # print(syn)
            i += 1
            added = syn
        else:
            added = symbols
        new_text += added
        percent = round((i+1)/(len(list_text)+1)*100)
        yield percent
    yield new_text

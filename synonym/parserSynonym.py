# -*- coding: utf-8 -*-
from synonym import EngineSynonym, ExtraStaff
from string import ascii_letters

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
        if x.isalpha() or x == '\'':
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
app.add_site_ru(ExtraStaff.create_urls_synonymonline, ExtraStaff.get_synonyms_synonymonline)
app.add_site_ru(ExtraStaff.create_urls_sinonim, ExtraStaff.get_synonyms_sinonim)
app.add_site_en(ExtraStaff.create_urls_thesaurus, ExtraStaff.get_synonyms_thesaurus)


def easter_egg(word):
    word = word.lower().replace('ё', 'е')
    if word in {'леня', 'леонид', 'ленчик', 'калачиков', 'чичиков'}:
        return 'Крутой'
    if word in {'антон', 'антоша', 'антошка', 'антончик', 'шевцов'}:
        return 'Лох'


def main(text):
    new_text = ''
    list_text = convert_string2list(text)
    for i in range(len(list_text)):
        symbols = list_text[i]
        egg = easter_egg(symbols)
        if egg is not None:
            added = egg
        elif len(symbols) <= 2 or not symbols.isalpha():
            added = symbols
        else:
            i += 1
            if symbols[0] in ascii_letters:
                syn = app.get_en(symbols)
            else:
                syn = app.get_ru(symbols)
            if symbols.isupper():
                syn = syn.upper()
            elif symbols.istitle():
                syn = syn.capitalize()
            elif symbols.islower():
                syn = syn.lower()
            added = syn
        new_text += added
        percent = round((i+1)/(len(list_text)+1)*100)
        yield percent
    yield new_text

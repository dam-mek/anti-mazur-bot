from lxml import html


def create_urls_synonymonline(word):
    word = word.replace('ё', 'е').replace('Ё', 'Е')
    return 'https://synonymonline.ru' + '/' + word[0].upper() + '/' + word


def get_synonyms_synonymonline(site):
    site = html.fromstring(site)
    synonyms = site.xpath('.//ol[@class="synonyms-list row"]/li/span/text()')
    words = []
    for i in range(min(5, len(synonyms))):
        if len(synonyms[i].split()) == 1:
            words.append(synonyms[i])
    return words


def create_urls_sinonim(word):
    return 'https://sinonim.org' + '/s/' + word


def get_synonyms_sinonim(site):
    site = html.fromstring(site)
    synonyms = site.xpath('.//table/tr/td[2]/a/text()')
    words = []
    for i in range(min(5, len(synonyms))):
        if len(synonyms[i].split()) == 1:
            words.append(synonyms[i])
    if words:
        return words


def create_urls_thesaurus(word):
    return 'https://www.thesaurus.com/browse/' + word


def get_synonyms_thesaurus(site):
    site = html.fromstring(site)
    synonyms = site.xpath('.//ul[@class="css-17d6qyx-WordGridLayoutBox et6tpn80"]/li/span/a/text()')
    words = []
    for i in range(min(5, len(synonyms))):
        if len(synonyms[i].split()) == 1:
            words.append(synonyms[i])
    if words:
        return words


def convert_link_wiki(a):
    a = a.split()
    return '/' + a[1] + ',_' + a[0]


def convert_link_wiki1(a):
    a = a.split()
    return '/' + a[0] + '_' + a[1]


def convert_link_wiki2(a):
    return '/' + a.replace(' ', '_')


def convert_link_google(a):
    return a.replace(' ', '+') + '+это'


def post_google(site):
    definition = ''
    DOM = html.fromstring(site)
    try:
        pp = DOM.xpath('.//span[@class="ILfuVd"]')[0]
    except IndexError:
        return ''
    for span in pp.getchildren():
        span = html.tostring(span, encoding='unicode')
        quotes = 0
        for symbol in span:
            if symbol in '<[({':
                quotes += 1
            if symbol in '>])}':
                quotes -= 1
                continue
            if not quotes:
                definition += symbol
    return definition


def post_wiki(site):
    definition = ''
    DOM = html.fromstring(site)
    try:
        p = DOM.xpath('.//div[@class="mw-parser-output"]/p')[0]
    except IndexError:
        return ''
    p = html.tostring(p, encoding='unicode')
    quotes = 0
    for symbol in p:
        if symbol in '<[({':
            quotes += 1
        if symbol in '>])}':
            quotes -= 1
            continue
        if not quotes:
            definition += symbol
    return definition

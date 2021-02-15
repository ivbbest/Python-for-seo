# Спарсить текст со страницы https://en.wikipedia.org/wiki/Neil_Armstrong.
# Достать из текста все имена существительные. Составить из них отсортированную таблицу частотности.
# Разложить текст на биграммы. Отфильтровать биграммы так, чтобы в результате были только такие биграммы,
# которые начинаются с имен существительных. Биграммы отсортировать по алфавиту и записать в txt файл.

from string import punctuation
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.util import ngrams
import re
from nltk.stem import WordNetLemmatizer
from requests_html import HTMLSession

url = 'https://en.wikipedia.org/wiki/Neil_Armstrong'
STOP_WORDS = set(stopwords.words('english'))

# вытаскиваем весь текст, а затем все существительные из текста
# в txt - весь текст, в nouns - все существительные

with HTMLSession() as session:

    resp = session.get(url)
    txt = resp.html.xpath('//div[@id="bodyContent"]')[0].text
    txt.replace("\n", "")
    txt = re.sub(r'\[\d\d\d?\d?\]', '', txt)

    nouns = [token for token, pos in pos_tag(word_tokenize(txt)) if pos.startswith('N')]


# считаем частотность существительных, используем лемматизацию

lemmatizer = WordNetLemmatizer()
frequency_nouns = {}

for word in nouns:

    lem_word = lemmatizer.lemmatize(word)

    if (lem_word in STOP_WORDS) or (lem_word in punctuation):
        continue

    if lem_word in frequency_nouns:
        frequency_nouns[lem_word] += 1
    else:
        frequency_nouns[lem_word] = 1

# берем ТОП-30 существительных из всего списка

popular_nouns = sorted(frequency_nouns.items(), key=lambda x: x[1], reverse=True)[:30]
print(popular_nouns)

# теперь будем считать биграммы, но в начале очистим текст от стоп слов и пунктуации

words = word_tokenize(txt)
cleaned_words = []

for word in words:

     if (word.lower() in STOP_WORDS) or (word.lower() in punctuation) \
             or ('ref' in word.lower()) or ('wikipedia' in word.lower())\
             or ('article' in word.lower()) or ('identifier' in word.lower()):
         continue

     cleaned_words.append(word.lower())

phrases = ngrams(cleaned_words, 2)

phrases = [' '.join(gr) for gr in phrases]

frequency_phrases = {}

for ph in phrases:

    if ph.split()[0] not in nouns:
        continue

    if ph in frequency_phrases:
        frequency_phrases[ph] += 1
    else:
        frequency_phrases[ph] = 1

popular_bigramm = sorted(frequency_phrases.items(), key=lambda x: x[1], reverse=True)

# запись биграмм в файл

with open('bigram_nouns.txt', 'w', encoding='utf-8') as f:

     for bigram in popular_bigramm:
         print(bigram, file=f)
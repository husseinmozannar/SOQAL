# -*- coding: utf-8 -*-
# This is Python 3.6
import json
import re
from polyglot.text import Text  # read README for how to install
ARABIC_LETTERS = 'ابتةثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ'


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def donwload_all_transliterators():
    from polyglot.downloader import downloader
    downloader.download("TASK:transliteration2", quiet=False)

def keep_only_arabic(file_name, last_article_name, first_article_name = ""):
    # last_article_name is the first article that is not in Arabic, remove everything after and including
    with open(file_name) as f:
        dataset = json.load(f)  # ['data']
    last_index = 0
    first_index = 0
    for article in dataset:
        if article['title'] == last_article_name:
            break
        last_index += 1

    if first_article_name != "":
        for article in dataset:
            if article['title'] == first_article_name:
                break
            first_index += 1
    print(last_index-first_index)
    dataset = dataset[first_index:last_index]
    with open(file_name[:-5] + "-only-arabic.json", 'w') as fp:
        json.dump(dataset, fp)

def transliterate_to_arabic(text):
    # takes in a string
    words = re.findall(r"[\w']+|[.,،!?;]", text)
    # words = text.split(" ")
    # transliterate each word alone
    tr_words = []
    for word in words:
        if is_arabic(word) or has_numbers(word) or word.isupper():
            tr_words.append(word)
            continue
        if word == "" or word == "." or word == "," or word == "،":
            tr_words.append(word)
            continue
        word_poly = Text(word)
        try:
            tr_word = word_poly.transliterate("ar")
        except:
            word = word.encode("ascii", errors="ignore").decode()
            tr_words.append(word)
            continue
        for w in tr_word:
            if not w == "":
                tr_words.append(w)
                break
    # combine
    tr_text = ""
    for w in tr_words:
        tr_text += " "
        tr_text += w

    return tr_text[1:]  # just to remove whitespace

def is_arabic(text):
    # takes in a string only!
    for letter in text:
        if ARABIC_LETTERS.find(letter) > 0:
            return True
    return False

def test_transliterate():
    test_text = " أدرجت الأحياء في ليفربول ، و Knowsley ، و St Helens و Sefton في ميرسيسايد. في مانشستر الكبرى كانت المقاطعات التالية هي بيري ، بولتون ، مانشستر ، أولدهام (جزء) ، روتشديل ، سالفورد ، تامسيد (جزء) ، ترافورد (جزء) ويجان. تمت إضافة وارينغتون و ويدنيس ، جنوب حدود ميرسيسايد / مانشستر الكبرى إلى مقاطعة شيشاير الجديدة غير الحضرية. أصبحت المناطق الحضرية في بارنولدزويك وإيربي ، مقاطعة باولاند الريفية وأبرشيات بريسويل وبروغدين وسالترفورث من مقاطعة سكيبتون الريفية في ويست رايدنج أوف يوركشاير جزءاً من لانكشاير الجديدة. وقد نُقلت رعية واحدة ، هي سيمونسوود ، من منطقة كنوسلي في ميرسيسايد إلى مقاطعة ويست لانكشاير في عام 1994. وفي عام 1998 ، أصبحت بلاكبول وبلاكبيرن مع داروين سلطات وحدوية مستقلة."
    print(transliterate_to_arabic(test_text))
    print(test_text)

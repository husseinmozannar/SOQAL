# This Python file uses the following encoding: utf-8
# This is Python2.7
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random
from google.cloud import translate
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c','--cred', help='Google Translate Credentials', required=True)
parser.add_argument('-s','--squad', help='Location of SQuAD to translate', required=True)

ARABIC_LETTERS = 'ابتةثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ'


def is_arabic(text):
    for letter in text:
        if ARABIC_LETTERS.find(letter) > 0:
            return True
    return False

def data_translate(filename):
    total_pars = 0
    total_quests = 0
    total_articles = 0
    with open(filename) as f:
        dataset = json.load(f)
    for article in dataset:
        print("Translating " + article['title'])
        if total_quests >= 8500:
            break
        for paragraph in article['paragraphs']:
            if (is_arabic(paragraph['context'])):
                print("Paragraph already in Arabic, skipping")
                continue
            else:
                print("Translating paragraph of " + article['title'])
            total_pars += 1
            to_print = random.randint(1, 6)  # don't always print
            if (to_print == 1):
                print(paragraph['context'])
            for qa in paragraph['qas']:
                total_quests += 1
                ans = "$$"
                for answer in qa['answers']:
                    if ans == "$$":
                        t = translate_text(answer['text'])
                        answer['text'] = t
                        ans = t
                    else:
                        answer['text'] = ans
                t = translate_text(qa['question'])
                qa['question'] = t
            t = translate_text(paragraph['context'])
            paragraph['context'] = t
            if (to_print == 1):
                print("######################################################")
                print("Translated text")
                print("######################################################")
                print(paragraph['context'])
        with open(filename, 'w') as fp:
            json.dump(dataset, fp)
        total_articles += 1
        print("######################################################")
        print("######################################################")
        print("Translated so far:")
        print("Number of articles: ", total_articles)
        print("Number of paragraphs: ", total_pars)
        print("Number of questions: ", total_quests)
        print("######################################################")
        print("######################################################")
    print("Finished Translation")


def translate_text(text):
    # The target language
    target = 'ar'
    # Translates text into Arabic using Neural Machine Translation
    translation = translate_client.translate(
        text,
        target_language=target, model=translate.NMT
    )

    translated_text = translation['translatedText']
    return translated_text


def main():
    args = parser.parse_args()
    translate_client = translate.Client.from_service_account_json(args.cred)
    data_translate(args.squad)

if __name__ == "__main__":
    main()

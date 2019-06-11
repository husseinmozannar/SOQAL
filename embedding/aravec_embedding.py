# -*- coding: utf8 -*-
import gensim
import re
import numpy as np
=
# =========================
# ==== Helper Methods =====

# Clean/Normalize Arabic Text
def clean_str(text):
    search = ["أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t',
              '&quot;', '?', '؟', '!']
    replace = ["ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ', ' ؟ ',
               ' ! ']

    # remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel, "", text)

    # remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    # trim
    text = text.strip()
    return text

## -- filter the existed tokens in a specific model
def get_existed_tokens(tokens, n_model):
    return [tok for tok in tokens if tok in n_model.wv]

def aravec_sentence_embedding(text, model_path):
    t_model = gensim.models.Word2Vec.load(MODEL_PATH)
    text_clean = clean_str(text).split(" ")
    text_tokens = get_existed_tokens(text_clean, t_model)
    vec = np.zeros(300)
    for token in text_tokens:
        token_vec = t_model.wv[token]
        vec += token_vec
    return vec

def test_aravec(model_path):
    a = aravec_sentence_embedding("مانشستر الكبرى إلى مقاطعة شيشاير الجديدة غير الحضرية . أصبحت المناطق الحضرية في بارنولدزويك وإيربي ، مقاطعة باولاند الريفية وأبرشيات بريسويل وبروغدين وسالترفورث من مقاطعة سكيبتون الريفية في ويست رايدنج أوف يوركشاير جزءا من لانكشاير الجديدة . وقد ن قلت رعية واحدة ، هي سيمونسوود ، من منطقة كنوسلي في ميرسيسايد إلى مقاطعة ويست لانكشاير في عام 1994 . وفي عام 1998 ، أصبحت بلاكبول وبلاكبيرن مع داروين سلطات وحدوية مستقلة .", model_path)
    print(a)

def main():
    model_path = "full_grams_cbow_300_wiki.mdl"
    test_aravec(model_path)

main()

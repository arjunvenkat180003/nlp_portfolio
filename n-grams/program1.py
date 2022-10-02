#Arjun Venkat - asv180003
#Arjun Balasubramanian - axb200075 

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import re
import pickle


def dict_builder(filename):
    
    with open(filename) as txt_file:
        content = txt_file.read()

        #print(content)

        content = re.sub('\n', '', content)

        #print(filename)
        #print(content)

        tokens = word_tokenize(content)

        unigrams = word_tokenize(content)
        bigrams = list(ngrams(tokens, 2))

        unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
        bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

        return unigram_dict, bigram_dict


eng_unigram_dict, eng_bigram_dict = dict_builder("ngram_files/LangId.train.English")
fr_unigram_dict, fr_bigram_dict = dict_builder("ngram_files/LangId.train.French")
ital_unigram_dict, ital_bigram_dict = dict_builder("ngram_files/LangId.train.Italian")

pickle.dump(eng_unigram_dict, open('uni_eng.p', 'wb'))  # write binary
pickle.dump(eng_bigram_dict, open('bi_eng.p', 'wb'))  # write binary
pickle.dump(fr_unigram_dict, open('uni_fr.p', 'wb'))  # write binary
pickle.dump(fr_bigram_dict, open('bi_fr.p', 'wb'))  # write binary
pickle.dump(ital_unigram_dict, open('uni_it.p', 'wb'))  # write binary
pickle.dump(ital_bigram_dict, open('bi_it.p', 'wb'))  # write binary

#dict_in = pickle.load(open('eng_unigram_dict.p', 'rb'))  # read binary
#print(dict_in)

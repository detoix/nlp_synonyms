import win32com.client as win32
import numpy as np
import gensim

def intersect(a, b):
    return list(set(a) & set(b))

def remove_punctuation(word):
    return word.lower().replace('.', '').replace(',', '').replace('\"', '').replace('(', '').replace(')', '').replace('-', '').replace('–', '')

def word():
    msword = win32.gencache.EnsureDispatch('Word.Application')
    selection = msword.Selection.Words
    document = msword.Documents(1).Words
    context = list(selection if len(selection) > 1 else document)
    model = gensim.models.Word2Vec.load('korpus_finansowy')

    text = ''
    words_array = np.asarray(context)
    words_array_lenth = len(words_array)
    for word_i, word in enumerate(words_array):
        word_s = str(word)
        word_string = word_s.rstrip()
        word_string_lowercase = word_string.lower()
        try:
            similar = model.similar_by_vector(word_string_lowercase, topn=100, restrict_vocab=None)
        except Exception as e:
            similar = []
        similar_list = [remove_punctuation(x[0]) for x in similar if x[1] > 0.60]

        if word_i is not 0 and word_i is not words_array_lenth - 1:
            local_context = [str(words_array[word_i-1]).rstrip(), str(words_array[word_i+1]).rstrip()]
            predicted = model.predict_output_word(local_context, topn=100) or []
            from_context = [remove_punctuation(w[0]) for w in predicted if w[1] > 0.000]
        else:
            from_context = []

        replacement = ''
        synonym_list = []
        for i in range(1, word.SynonymInfo.MeaningCount + 1):
            if i == 1:
                synonym_list.append(word_string_lowercase)

            for synonym in word.SynonymInfo.SynonymList(i):
                synonym_list.append(str(synonym))

        intersection_one = intersect(similar_list, synonym_list)
        intersection_two = intersect(from_context, synonym_list)
        intersection_three = intersect(similar_list[:10], from_context[:10])
        joined = intersection_one + intersection_two + intersection_three
        merged = [x for x in set(joined) if str(x).rstrip() != word_string_lowercase]

        for n, w in enumerate(merged):
            if n == 0:
                replacement += '{' + word_string

            w_cased = w.title() if word_string[0].isupper() else w
            replacement += '|' + w_cased
                
            if n == len(merged) - 1:
                replacement += '}'
                if ' ' in word_s:
                    replacement += ' '

        text += replacement or word_s

    msword.Selection.TypeText(text)

if __name__ == '__main__':
    word()

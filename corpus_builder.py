import gensim, logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Bankier(object):
    def __iter__(self):
        for line in open('korpus_finansowy.txt', encoding='utf8'):
            yield line.split()
            
model = gensim.models.Word2Vec(Bankier())
model.save('korpus_finansowy')

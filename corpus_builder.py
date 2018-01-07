import gensim, logging, os, json
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Bankier(object):
    def __iter__(self):
        for path, subdirs, files in os.walk('json_files'):
            for filename in files:
                with open('json_files\\' + filename, 'r') as file:
                    f = json.loads(file.read())
                    for line in f:
                        yield line['content'].split()
        
model = gensim.models.Word2Vec(Bankier())
model.save('korpus_finansowy')

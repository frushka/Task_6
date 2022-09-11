from re import compile, sub
import random
from pickle import dump, load
import sys


class TxtGen:
    '''The main class of the n-gram model'''

    @staticmethod
    def ExistenceFile(file, method='rb'):
        '''Method of exception handling
        when working with a file'''
        try:
            f = open(file, method)
        except IOError:
            print(f'File opening error:{file}')
            exit()
        else:
            return f

    @staticmethod
    def prefix(words):
        length = len(words)
        a, b = words[0], words[1]
        for i in range(3, length):
            c = words[i]
            yield a, b, c
            a, b = b, c

    def fit(self, mymodel, file=None, txt=''):
        '''Model training method'''
        if file != None:
            f = open(file, 'r', encoding='UTF-8')
            for string in f:
                txt += string
            f.close()
        else:
            print('Input text:')
            for line in sys.stdin:
                txt += line

        rules = compile('[^A-яё]')
        txt = rules.sub(' ', txt).lower().split(' ')
        txt = list(filter(lambda x: len(x) > 0, txt))
        pref = self.prefix(txt)
        self.modelCreate(list(pref), mymodel)

    @staticmethod
    def trainList(text):
        '''Method of creating a list
        from the source text'''
        rules = compile('[^A-яё]')
        text = rules.sub(' ', text).lower().split(' ')
        text = list(filter(lambda x: len(x) > 0, text))
        return text

    @staticmethod
    def modelCreate(prefix, mymodel) -> None:
        '''The method of creating a model according to the example'''
        gram2, gram3, model = {}, {}, {}

        for firstword, secondword, thirdword in prefix:

            if (firstword, secondword) not in gram2:
                gram2[firstword, secondword] = 0
            gram2[firstword, secondword] += 1

            if (firstword, secondword, thirdword) not in gram3:
                gram3[firstword, secondword, thirdword] = 0
            gram3[firstword, secondword, thirdword] += 1

        for (a, b, c), freq in gram3.items():
            if (a, b) in model:
                model[a, b].append((c, freq / gram2[a, b]))
            else:
                model[a, b] = [(c, freq / gram2[a, b])]

        file = open(mymodel, 'wb')
        dump(model, file)
        file.close()

    def generate(self, mymodel, prefix, length) -> list:
        '''Method that generates new text'''

        with open(mymodel, 'rb') as file:
            model = load(file)

        nword, txt = None, []

        if prefix:
            txt = prefix.lower().split(' ').copy()
            last = txt[-1]

            for word in model.keys():
                if last in word and word[0] == last:
                    nword = word

        if nword is None:
            return list("Unable to generate a phrase".split(' '))

        Len = len(txt)
        if length > Len:
            txt.append(nword[1])
            for i in range(length - Len - 2):
                nextWord = random.choices([word for (word, freq) in model[nword]],
                                       weights=[freq for (word, freq) in model[nword]])
                txt.append(nextWord[0])
                nword = (nword[1], nextWord[0]) if (nword[1], nextWord[0]) in model else random.choice(list(model.keys()))
        return txt





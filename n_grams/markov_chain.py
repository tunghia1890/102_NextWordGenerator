from collections import defaultdict, Counter
from preprocessing import text_preprocessing


class NextWordGen:
    def __init__(self):
        self.lookup_dict = defaultdict(list)

    @staticmethod
    def __generate_tuple_keys(input_lines, n_grams=1):
        for sent in input_lines:
            sent = sent.rsplit()
            if len(sent) < n_grams:
                return
            for i in range(len(sent) - n_grams):
                if n_grams == 1:
                    yield [sent[i], sent[i+1]]
                elif n_grams == 2:
                    yield [sent[i], sent[i + 1], sent[i + 2]]
                elif n_grams == 3:
                    yield [sent[i], sent[i + 1], sent[i + 2], sent[i + 3]]

    def add_document(self, input_lines):
        pairs = self.__generate_tuple_keys(input_lines=input_lines, n_grams=1)
        for pr in pairs:
            self.lookup_dict[tuple([pr[0]])].append(pr[1])

        pairs_two = self.__generate_tuple_keys(input_lines=input_lines, n_grams=2)
        for pr in pairs_two:
            self.lookup_dict[(pr[0], pr[1])].append(pr[2])

        pairs_three = self.__generate_tuple_keys(input_lines=input_lines, n_grams=3)
        for pr in pairs_three:
            self.lookup_dict[(pr[0], pr[1], pr[2])].append(pr[3])

        # print(self.lookup_dict)

    def generate_text(self, word):
        for n in [-3, -2, -1]:
            word_ngram = tuple(word.rsplit())[n:]
            if (len(word_ngram) == abs(n)) and (word_ngram in self.lookup_dict):
                print(f'{abs(n)}-gram', word_ngram)
                return Counter(self.lookup_dict[word_ngram]).most_common(n=3)
        return []


def input_test():
    markov_chain = NextWordGen()
    pp = text_preprocessing.Preprocessing()
    markov_chain.add_document(input_lines=pp.get_corpus())

    while True:
        word = input('word: ')
        if word == ':q':
            break
        result = markov_chain.generate_text(word=word.strip())
        print(result)


if __name__ == '__main__':
    input_test()

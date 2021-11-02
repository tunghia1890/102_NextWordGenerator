import re
import pickle


def raw_processing(paragraph: str, is_log=False):
    sentences = []
    paragraph_split = re.split(r'([.,\n])', paragraph)

    if is_log:
        total = len(paragraph_split)
        count = 0

    for sent in paragraph_split:
        sent = sent.lower()
        sent = re.sub(r"(v\.v\.|[0-9-:)\"(/–])", ' ', sent, flags=re.I | re.M | re.S)
        sent = re.sub(r'( +)', r' ', sent, flags=re.I | re.M | re.S)
        sent = sent.strip()
        if (len(sent) > 6) and (' ' in sent):
            sentences.append(sent)

        if is_log:
            if (count % int(total/10)) == 0:
                print(f'{int(100 * count / total)}%', end=' ')
            count += 1
    print('')
    return sentences


def get_ngram_keys(sentences, n_grams=1):
    for sent in sentences:
        sent = sent.rsplit()
        if len(sent) < n_grams:
            return
        for i in range(len(sent) - n_grams):
            if n_grams == 1:
                yield [sent[i], sent[i + 1]]
            elif n_grams == 2:
                yield [sent[i], sent[i + 1], sent[i + 2]]
            elif n_grams == 3:
                yield [sent[i], sent[i + 1], sent[i + 2], sent[i + 3]]


def add_counter_dict(count_dict, key, value):
    if key in count_dict:
        if value in count_dict[key]:
            count_dict[key][value] += 1
        else:
            count_dict[key][value] = 1
    else:
        count_dict[key] = {value: 1}
    return count_dict


def get_next_word_dict(sentences):
    next_work_dict = {}
    pairs = get_ngram_keys(sentences=sentences, n_grams=1)
    for pr in pairs:
        next_work_dict = add_counter_dict(count_dict=next_work_dict,
                                          key=tuple([pr[0]]), value=pr[1])

    pairs_two = get_ngram_keys(sentences=sentences, n_grams=2)
    for pr in pairs_two:
        next_work_dict = add_counter_dict(count_dict=next_work_dict,
                                          key=(pr[0], pr[1]), value=pr[2])

    pairs_three = get_ngram_keys(sentences=sentences, n_grams=3)
    for pr in pairs_three:
        next_work_dict = add_counter_dict(count_dict=next_work_dict,
                                          key=(pr[0], pr[1], pr[2]), value=pr[3])
    return next_work_dict


def max_value(count_dict):
    count_list = list(count_dict.items())
    if len(count_list) == 0:
        return ''

    count_list.reverse()
    print(count_list)
    max_key, max_val = count_list[0]
    for key, val in count_list[1:]:
        if val > max_val:
            max_key, max_val = key, val
    return max_key


def inference(next_word_dict, last_sentence):
    result = {}
    for n in [-3, -2, -1]:
        word_ngram = tuple(last_sentence.rsplit())[n:]
        if (len(word_ngram) == abs(n)) and (word_ngram in next_word_dict):
            print(f'{abs(n)}-gram', word_ngram)
            result = next_word_dict[word_ngram]
            break

    # next_word = max_value(result)

    result = list(result.items())
    result.sort(key=lambda x: x[1], reverse=True)

    next_word = result[0] if len(result) > 0 else ''
    return result[:10], next_word


def ngram_from_paragraph(paragraph):
    sentences = raw_processing(paragraph=paragraph)
    next_word_dict = get_next_word_dict(sentences=sentences)
    last_sentence = paragraph.split('.')[-1].lower().strip()
    result, next_word = inference(next_word_dict=next_word_dict, last_sentence=last_sentence)
    return result, next_word


class NextWordCorpus:
    instance = None

    @staticmethod
    def get_instance():
        if not NextWordCorpus.instance:
            NextWordCorpus.instance = NextWordCorpus()
        return NextWordCorpus.instance

    def __init__(self):
        self.data_path = 'data/VNESEcorpus.txt'
        with open(self.data_path, 'r', encoding='utf8') as f:
            paragraph = f.read()
        print('Loading ...')
        sentences = raw_processing(paragraph=paragraph, is_log=True)
        self.next_word_dict = get_next_word_dict(sentences=sentences)

        with open('next_word_corpus.pkl', 'wb') as f:
             pickle.dump(self.next_word_dict, f)
        print('Done!')

    def ngram_from_corpus(self, input_paragraph):
        last_sentence = input_paragraph.split('.')[-1].lower().strip()
        result, next_word = inference(next_word_dict=self.next_word_dict, last_sentence=last_sentence)
        return result, next_word


def testing():
    import time
    tic = time.time()
    if True:
        paragraph = """Máy tính hay máy điện toán máy điện toán máy điện là một máy \ncó thể được hướng dẫn để thực hiện các chuỗi các phép toán số học hoặc logic một cách tự động thông qua lập trình máy tính . 
    Máy tính   """
    result, next_word = ngram_from_paragraph(paragraph=paragraph)
    print(result)
    print(next_word)
    print('cost', time.time() - tic)

    while True:
        word = input('word: ')
        if word == ':q':
            break
        tic = time.time()
        result, next_word = NextWordCorpus.get_instance().ngram_from_corpus(input_paragraph=word)
        print(result)
        print(next_word)
        print('cost', time.time() - tic)


if __name__ == '__main__':
    testing()

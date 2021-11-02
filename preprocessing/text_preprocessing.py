import re


class Preprocessing:
    def __init__(self):
        self.content_path = '../data/computer.txt'
        self.pred_path = '../data/computer_pred.txt'

    @staticmethod
    def remove_spec(sent):
        sent = re.sub(r"(v\.v\.|[0-9-:)\"(/–])", ' ', sent, flags=re.I | re.M | re.S)
        sent = re.sub(r'( +)', r' ', sent, flags=re.I | re.M | re.S)
        return sent

    def preprocess(self, is_write=False):
        if is_write:
            out_file = open(self.pred_path, 'w', encoding='utf8')

        with open(self.content_path, 'r', encoding='utf8') as f:
            count = 0
            for line in f.readlines():
                line = line.strip().lower()
                print('')
                print(count, 'Before:', line)
                line_split = re.split(r'([.,])', line)
                for sent in line_split:
                    sent = self.remove_spec(sent=sent)
                    sent = sent.strip()
                    if (len(sent) > 6) and (' ' in sent):
                        print(count, 'Afters:', sent)
                        if is_write:
                            out_file.write(sent + '\n')
                count += 1

        if is_write:
            out_file.close()

    def get_corpus(self):
        with open(self.pred_path, 'r', encoding='utf8') as f:
            lines = []
            for li in f.readlines():
                lines.append(li.strip())
        return lines


if __name__ == '__main__':
    pp = Preprocessing()
    pp.preprocess(is_write=True)

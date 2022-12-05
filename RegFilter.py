import re
from trieregex import TrieRegEx as TRE
from wulgaryzmy import wulgaryzmy


class RegFilter:
    replace_dict = {'i': '1l', 'e': '3', 'w': 'v', 'a': '@4', 'o': '0', 'u': 'v', 'l': 'i'}

    def __init__(self):
        self.reg = None

    def check_phrase(self, phrase: str):
        changed_phrase = phrase.lower()
        changed_phrase = re.sub(re.compile('\s|\W[^@]]'), '_', changed_phrase)
        changed_phrase = re.sub(self.reg, self.star_counter, changed_phrase)
        new_phrase = ''
        for i, l in enumerate(changed_phrase):
            new_phrase += phrase[i] if changed_phrase[i] != '*' else '*'
        return new_phrase

    def star_counter(self, match_obj: re.Match):
        kek = match_obj.span()
        ignore = 0
        if match_obj.string[kek[1]-1] == '_':
            ignore = 1
        to_replace = '*'*(kek[1] - kek[0] - ignore) + '_'*ignore
        return to_replace

    def load_regex(self):
        with open('baked.txt', 'r') as f:
            reg = f.read()
        self.reg = re.compile(reg)
        return self

    def bake_regex(self, words):
        words_extended = self._words_super_extender(words)
        reg = "|".join(words_extended)
        regexed_words = reg.split('|')
        tre = TRE(*regexed_words)
        reg = tre.regex()
        reg = self._add_empty(reg)
        reg = self._replace_letters(reg)

        print(reg)
        with open('baked.txt', 'w') as f:
            f.write(reg)
        self.reg = re.compile(reg)
        return self

    def _replace_letters(self, reg):
        for key in list(self.replace_dict.keys()):
            reg = re.sub(re.compile(key + '(?!(?!\[)(?:.(?!\[))*\])'), '['+key+self.replace_dict[key]+']', reg)
        return reg

    def _add_empty(self, reg):
        reg = re.sub(re.compile('\w(?!(\|)|(\]))'), self._extend_char, reg)
        return reg

    def _extend_char(self, match_obj: re.Match):
        span = match_obj.span()
        return (match_obj.string[span[0]: span[1]] + '+_?')

    def _words_super_extender(self, words_list):
        words_to_add = []
        for word in words_list:
            words_to_add = words_to_add + self._word_extender(word) + [word]

        return words_to_add

    def _word_extender(self, word):
        new_words = []
        for i, l in enumerate(word):
            word_len = len(word)-1
            if i not in [0, word_len]:
                new_words.append(word[:i] + word[i+1] + word[i] + word[i+2:])
            elif i == 0:
                new_words.append(word[i + 1] + word[i] + word[i + 2:])
        return new_words


if __name__ == '__main__':
    my_filter = RegFilter().bake_regex(wulgaryzmy)
    phrase = 'Twoja stara to chuj i zaje#b1śCi3, cchuuuj, kurwi#ska, cuhj, kurvviszonem, cip@, spierdaia, jebal'
    print(phrase)
    print(my_filter.check_phrase(phrase))

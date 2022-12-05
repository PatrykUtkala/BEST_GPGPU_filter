import re
from trieregex import TrieRegEx as TRE
from wulgaryzmy import wulgaryzmy
import warnings
warnings.filterwarnings("ignore")
words = wulgaryzmy
replace_dict = {'i': '1L', 'e': '3', 'w': 'v', 'a': '@4', 'o': '0', 'u': 'v'}


class RegFilter:
    def __init__(self):
        self.reg = None

    def check_phrase(self, phrase: str):
        changed_phrase = phrase.lower()
        changed_phrase = re.sub(re.compile('\s|\W'), '_', changed_phrase)
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

    def bake_regex(self):
        words_extended = self._words_super_extender(words)
        # print(words_extended)
        reg = "|".join(words_extended)
        # print(reg)
        regexed_words = reg.split('|')
        tre = TRE(*regexed_words)
        reg = tre.regex()
        # print(reg)
        reg = self._add_empty(reg)
        # print(reg)
        reg = self._replace_letters(reg)

        print(reg)
        with open('baked.txt', 'w') as f:
            f.write(reg)
        self.reg = re.compile(reg)
        return self

    def _replace_letters(self, reg):
        for key in list(replace_dict.keys()):
            reg = reg.replace(key, '['+key+replace_dict[key]+']')
        return reg

    def _add_empty(self, reg):
        reg = re.sub(re.compile('\w(?!\|)'), self._extend_char, reg)
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
    my_filter = RegFilter().load_regex()
    phrase = 'Twoja stara to chuj i zaje#b1śCi3, cchuuuj, kurwi#ska, cuhj, kurvviszonem'
#     phrase = '''W dobie internetu coraz częściej spotykamy się z filtrowaniem komentarzy czy czatu pod
# kątem treści obraźliwych. W przypadku wielu stron wynika to z konieczności utrzymania
# odpowiedniego poziomu kultury, ze względu na wymagania reklamodawców, którzy nie
# chcą, by ich marka była kojarzona z “nieodpowiednimi środowiskami”. Mimo to, używane
# obecnie filtry wciąż nie działają perfekcyjnie - ich twórcy, chcąc ograniczyć ilość przypadków
# “false positive”, często poprzestają na ograniczonych rozwiązaniach. Ponadto, sprawy nie
# ułatwiają użytkownicy internetu, którzy chcąc obejść cenzurę, korzystają ze sztuczek takich
# jak zastępowanie w słowach niektórych liter podobnie wyglądającymi znakami, czy pisaniem
# w nie do końca poprawnie gramatyczny sposób. W wyniku tego problem usuwania treści
# obraźliwych, początkowo trywialny, staje się znacznie trudniejszy (przykładowo,
# wprowadzony jakiś czas temu filtr czatu w jednej z popularnych gier, nie pozwalał na użycie
# słowa night z powodu rzekomego podobieństwa do pewnego bardzo nieładnego słowa).'''
    print(phrase)
    print(my_filter.check_phrase(phrase))

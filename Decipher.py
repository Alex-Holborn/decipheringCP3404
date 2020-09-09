import Data
import CrackedPair
class Decipher:

    def __init__(self, cipher):
        d = Data.Data()
        self.cipher = cipher
        self.clean_cipher = self.sanitise_input(self.cipher, d.punctuation)
        self.letter_by_freq = self.create_char_dictionary(self.clean_cipher, False, d.alphabet)
        self.word_by_freq = self.create_word_dictionary(self.clean_cipher.split(" "))
        self.unused_letters = self.get_unused_letters(self.clean_cipher, d.alphabet)
        self.most_used_char_array = self.sort_dict_to_array(self.letter_by_freq)
        self.most_used_word_array = self.sort_dict_to_array(self.word_by_freq)
        self.cracked_letters = {}
        self.cracked_pairs = {}

        for char in d.alphabet:
            self.cracked_pairs[char] = CrackedPair.CrackedPair(char)

        # first, let's find instances where letters double up in the cipher, but only keep one of each letter
        doubles = []
        prev = ''
        for char in self.clean_cipher:
            if prev == char:
                doubles.append(char)
            prev = char
        #print(doubles)

        # now any letter that does not occur naturally (or very rarely) as a double can be excluded as a pair for any doubled letter
        excludes = "ahijkquvwxyz"
        for char in doubles:
            for c in excludes:
                self.cracked_pairs[char].add_impossible_pair(c)

        # now lets assign any unused letters to the most infrequently used letters
        for i, char in enumerate(self.unused_letters):
            self.cracked_pairs[char].paired_char = d.letters_by_freq[d.letters_by_freq.__len__() - (1 + i)]
            for char in self.cracked_pairs.keys():
                self.cracked_pairs[char].add_impossible_pair(self.cracked_pairs[self.unused_letters[i]].paired_char)

        # lets assume the most common letter is an e
        e = self.most_used_char_array[0]
        self.cracked_pairs[e].paired_char = 'e'

        # now let's exclude e from every other char
        for char in self.cracked_pairs.keys():
                self.cracked_pairs[char].add_impossible_pair('e')

        # 'the' is probably the most common 3 letter word that appears, lets find the most common 3 letter word with an e at the end
        the = self.translate_to_cipher("the")
        found_the = self.find_words_with_phrase(self.word_by_freq, the, 3)
        if found_the:
            self.cracked_pairs[found_the[0][0]].set_paired_char('t')
            self.cracked_pairs[found_the[0][1]].set_paired_char('h')

        word_lists = d.words
        for i in range(0, 5):
            for word_list in word_lists:
                self.search_for_words_in_cipher(self.word_by_freq, word_list, True)

        #self.display_pairs_debug()
        self.display_result()
        #self.display_result(False)

    def find_wildcard_matches(self, cipher_words, search_term, restrict_to_full_words=True):
        if restrict_to_full_words:
            return self.find_words_with_phrase(cipher_words, search_term, search_term.__len__())
        return self.find_words_with_phrase(cipher_words, search_term)

    def search_for_words_in_cipher(self, cipher_words, search_words, restrict_to_full_words=True):
        ##takes words and translates them into the cipher and then searches for them

        #TODO: this needs re writing so we can take words containing the search_term and fill parts of it in
        for word in search_words:
            translation = self.translate_to_cipher(word)
            indexes = []
            for i, char in enumerate(translation):
                if char == '?':
                    indexes.append(i)
            chars = []
            for i in indexes:
                chars.append(word[i])
            #print("{} {} {}".format(word, indexes, chars))
            duplicates_only = self.are_all_chars_same(chars)
            search_results = self.find_wildcard_matches(cipher_words, translation, restrict_to_full_words)
            #print("searching for {} - translates to {} - found {}".format(word, translation, search_results))
            if not restrict_to_full_words:
                for result in search_results:
                    length = translation.__len__()
                    for i, char in enumerate(result):
                        if i + length <= result.__len__():
                            s = ""
                            for j in range(0 + i, i + length):
                                s += result[j]
                            if s == translation:
                                result = s
                                print(result)
            if search_results:
                if self.does_word_contain_char(translation, '?'):
                    if self.get_amount_of_char_in_word(translation, '?') == 1 or (duplicates_only and self.get_amount_of_char_in_word(translation, '?') > 1):
                        for i, char in enumerate(translation):
                            if char == '?':
                                letter = word[i]
                                #print(i)
                                chars = ""
                                for _word in search_results:
                                    chars += self.cracked_pairs[_word[i]].paired_char
                                for _word in search_results:
                                    if self.cracked_pairs[_word[i]].paired_char == '?':
                                        if chars.__len__() == 1 or self.get_amount_of_char_in_word(chars, '?') == 1:
                                            self.cracked_pairs[_word[i]].set_paired_char(letter)
                                           # print("{} -> {} = {} -> {}".format(word, translation, search_results, _word))

    def are_all_chars_same(self, char_array):
        prev = ''
        for c in char_array:
            if prev == '':
                prev = c
            else:
                if c != prev:
                    return False
                prev = c
        return True

    def get_char_pos_in_array(self, array, char):
        for i, c in enumerate(array):
            if c == char:
                return i

    def does_word_contain_char(self, word, char):
        for c in word:
            if c == char:
                return True
        return False

    def get_amount_of_char_in_word(self, word, char):
        count = 0
        for c in word:
            if c == char:
                count += 1
        return count


    def has_char_been_solved(self, char):
        if char == '?': return False
        for k in self.cracked_pairs.keys():
            if self.cracked_pairs[k].paired_char == char:
                return True
        return False

    def create_char_dictionary(self, input, allow_spaces, alphabet):
        char_dict = {}
        for char in input:
            if char in alphabet:
                if (allow_spaces and char == " ") or char != " ":
                    if char in char_dict.keys():
                        char_dict[char] += 1
                    else:
                        char_dict[char] = 1
        return char_dict

    def create_word_dictionary(self, input):
        word_dict = {}
        for word in input:
            if word not in word_dict.keys():
                word_dict[word] = 1
            else:
                word_dict[word] += 1
        return word_dict

    def get_unused_letters(self, input, alphabet):
        unused = []
        for char in alphabet:
            if char not in input:
                unused.append(char)
        return unused

    def sanitise_input(self, cipher_input, regex):
        # removes unwanted characters (ie punctuation) from the inputted string and returns a clean string
        clean_cipher = ""
        for char in cipher_input:
            if char in regex:
                clean_cipher += ""
            else:
                clean_cipher += char
        return clean_cipher

    def get_words_of_length(self, length, word_list, allow_repeats):
        # returns words of parameter length from the word_list
        words = []
        for word in word_list:
            if word.__len__() == length:
                if (word not in words and not allow_repeats) or allow_repeats:
                    words.append(word)
        return words

    def get_words_containing_char(self, char, word_list):
        words = []
        for word in word_list:
            if char in word:
                words.append(word)
        return words

    def get_words_of_length_containing_char(self, length, char, word_list):
        return self.get_words_of_length(length, self.get_words_containing_char(char, word_list))

    def sort_dict_to_array(self, cypher_dict):
        # returns an array of chars ordered from most used to least used in the dictionary
        sorted = []
        for k, v in cypher_dict.items():
            if sorted.__len__() == 0:
                sorted.append(k)
            else:
                for i, letter in enumerate(sorted):
                    if letter != k:
                        if cypher_dict[letter] > cypher_dict[k]:
                            if i == sorted.__len__() - 1:
                                sorted.append(k)
                        else:
                            sorted.insert(i, k)
                            break
        return sorted

    def get_largest_word_in_list(self, word_list):
        _word = ""
        for word in word_list:
            if _word == "":
                _word = word
            else:
                if word.__len__() > _word.__len__():
                    _word = word
        return _word

    def get_most_common_word_in_dict(self, word_dict):
        _word = ""
        for word in word_dict.keys():
            if _word == "":
                _word = word
            else:
                if word_dict[word] > word_dict[_word]:
                    _word = word
        return _word

    def get_dict_of_words_of_length(self, length):
        # provides a sub-dictionary of main dictionary of words only of certain length
        words = {}
        for word in self.word_by_freq.keys():
            if word.__len__() == length:
                words[word] = self.word_by_freq[word]
        return words

    def get_suffixes_of_length(self, word_list, length):
        suffixes = {}
        for word in word_list:
            if word.__len__() > length:
                suffix = word[word.__len__() - length: word.__len__()]
                if suffix not in suffixes.keys():
                    suffixes[suffix] = 1
                else:
                    suffixes[suffix] += 1
        return suffixes

    def translate_to_cipher(self, word):
        s = ""
        for char in word:
            s += self.get_char_representative_in_cipher(char)
        return s

    def display_result(self, preserve_punctuation=True):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        new_cipher = ""
        prev = ' '
        next_capital = True
        for char in self.cipher:
            if not preserve_punctuation:
                if char in alphabet or char == ' ':
                    if char == ' ':
                        new_cipher += ' '
                    else:
                        new_cipher += self.cracked_pairs[char].paired_char
            else:
                if prev == '.':
                    next_capital = True
                if char in alphabet:
                    if next_capital:
                        new_cipher += self.cracked_pairs[char].paired_char.upper()
                        next_capital = False
                    else:
                        new_cipher += self.cracked_pairs[char].paired_char
                else:
                    new_cipher += char
            prev = char
        print(new_cipher)

    def get_char_representative_in_cipher(self, char):
        #takes a char and translates it into cipher speak, if we have found a match for it. otherwise returns '?'
        if char == '?': return '?'
        for k in self.cracked_pairs.keys():
            if self.cracked_pairs[k].paired_char == char:
                return self.cracked_pairs[k].representing_char
        return '?'

    def display_pairs_debug(self):
        for c in self.cracked_pairs.keys():
            if self.cracked_pairs[c].is_char_paired():
                print("[{}]SOLVED CHAR = {}".format(c,
                                                   self.cracked_pairs[c].paired_char))
            else:
                print("[{}] Cant be : {}".format(c, self.cracked_pairs[c].impossible_pairs))

    def find_words_with_phrase(self, word_list, phrase, size_limit=-1):
        # phrase is a string with possible '?' wildcard chars
        # this function searches for all words containing the phrase and returns an array of all relevant words
        # size of words returned can be limited by optional parameter size_limit
        # will return an empty array if no suitable words found
        words = []
        nonWildcardIndexes = []
        for i, char in enumerate(phrase):
            if phrase[i] != '?':
                nonWildcardIndexes.append(i)
        _words = []
        if nonWildcardIndexes.__len__() > 0:
            _words = self.get_words_containing_char(phrase[nonWildcardIndexes[0]], word_list)
        for word in _words:
            if (word.__len__() >= phrase.__len__() and size_limit == -1) or (word.__len__() >= phrase.__len__() and word. __len__() <= size_limit):
                # now iterate through word looking for phrase
                for i in range(0, word.__len__() - (phrase.__len__() - 1)):
                    # this is the base for iterating through
                    s = ""
                    for j in range(0, phrase.__len__()):
                        s += word[j + i]
                    letters_matched = 0
                    for index in nonWildcardIndexes:
                        if phrase[index] != '?':
                            if phrase[index] == s[index]:
                                letters_matched += 1
                    if letters_matched == nonWildcardIndexes.__len__():
                        words.append(word)
        return words


Decipher("tigcsvqhpi hj qat vchbhqhet gcsvqplcfvahg pvtcfqhpi xjtm qp tijxct jtgctgs pc gpizhmtiqhfohqs pz " +
         "hizpcbfqhpi qcfijbhqqtm fgcpjj fi xijtgxctm gpbbxihgfqhpi gafiito. qat tigcsvqhpi pvtcfqhpi qfutj f vhtgt pz" +
         " hizpcbfqhpi, fojp gfootm btjjflt pc vofhiqtkq, fim qcfijzpcbj hq hiqp f gcsvqplcfb pc ghvatcqtkq xjhil f "+
         "jtgctq gcsvqplcfvahg uts. mtgcsvqhpi hj qat ctetcjt pvtcfqhpi qp tigcsvqhpi. qat ctgthetc dap apomj qat gpcctgq"+
         " jtgctq uts gfi ctgpetc qat btjjflt (vofhiqtkq) zcpb qat gcsvqplcfb (ghvatcqtkq).")

Decipher("bftuhq, hornfb rgk rklunrg hopcuk opc qou zrdqpbfhrqfpg wbpilun dpxlk iu xhuk qp dpghqbxdq r wxilfd-vus " +
         "dbswqphshqun (qofh fh qou cull-vgpcg bhr dbswqphshqun). nubvlu rgk oullnrg xhuk qou vgrwhrdv wbpilun fg qoufb"+
        " dpghqbxdqfpg. ndulfudu ixflq r hshqun cofdo rwwlfuk ubbpb dpbbudqfge dpkuh. lrqub fg 1985, ulernrl kuhfeguk "+
         "r wxilfd-vus dbswqphshqun xhfge qou kfhdbuqu lperbfqon wbpilun. nfllub rgk vpilfqy hxeeuhquk xhfge ullfwqfd "+
         "dxbtuh qp kuhfeg wxilfd-vus dbswqphshqunh.")

Decipher("vehmdrt-uts (dnkq gdnnto ksbbtrehg) gesvrqkskrtbk wkt rct kdbt ktgetr uts zqe tjgesvrhqj djo otgesvrhqj. "+
         "dnrcqwyc rct tjgesvrhqj djo otgesvrhqj utsk oq jqr jtto rq it hotjrhgdn, rct ujqfntoyt qz qjt qz rctb "+
         "kwzzhgtk rq qirdhj rct qrcte. vwinhg-uts (dnkq gdnnto dksbbtrehg) gesvrqkskrtbk wkt d ohzztetjr uts zqe "+
         "tjgesvrhqj djo otgesvrhqj. rct ujqfntoyt qz qjt uts, cqftmte, oqtk jqr dnnqf rct qrcte rq it otrtebhjto.it")

Decipher("gq dtj mxgfvrs cutrgyul qatq qau tjjxbwqgph pz th gehpcthq tqqtfvuc dtj hpq cutrgjqgf. bpjq utcrs uxcpwuth"+
         " fcswqpjsjqubj ducu lujgehul qp dgqajqthl qau tqqtfvj pz ulxftqul pwwphuhqj dap vhud qau uhfcswqgph wcpfujj,"+
         " nxq lgl hpq vhpd qau fcswqpectwagf vus. tllgqgphtrrs, gq dtj cumxujqul qatq qau uhfcswqgph thl lufcswqgph "+
         "wcpfujjuj fpxrl nu lphu mxgfvrs, xjxtrrs ns athl, pc dgqa qau tgl pz bufathgftr luigfuj jxfa "+
         "tj qau fgwauc lgjv ghiuhqul ns ruph ntqqgjt trnucqg.")
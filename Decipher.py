import Data
import CrackedPair
import time


class Decipher:

    def __init__(self, cipher):
        start_time = time.time()
        self.words_used = 0
        self.data = Data.Data()
        self.cipher = cipher
        self.clean_cipher = self.sanitise_input(self.cipher, self.data.punctuation)
        self.letter_by_freq = self.create_char_dictionary(self.clean_cipher, False, self.data.alphabet)
        self.word_by_freq = self.create_word_dictionary(self.clean_cipher.split(" "))
        self.unused_letters = self.get_unused_letters(self.clean_cipher, self.data.alphabet)
        self.most_used_char_array = self.sort_dict_to_array(self.letter_by_freq)
        self.most_used_word_array = self.sort_dict_to_array(self.word_by_freq)
        self.cracked_pairs = {}

        for char in self.data.alphabet:
            self.cracked_pairs[char] = CrackedPair.CrackedPair(char)

        if not self.solve_most_common_characters(self.data):
            print("failed to determine most common characters/words (if you are reading this I messed up)")
            exit()

        word_lists = self.data.words
        for i in range(0, 2):
            for word_list in word_lists:
                self.search_for_words_in_cipher(self.word_by_freq, word_list)
        for word_list in word_lists:
            self.review_substring_patterns(self.word_by_freq, word_list)

        self.fill_unused_chars()
        print(self.cipher)
        print("\n")
        self.display_result(start_time, True, True)
        print("\n")
        self.display_grid(True)
        print("\n")
        self.get_rep_char_grid()

        print("Unused cipher letters: {}".format(self.unused_letters))
        print("\n")
        # self.display_pairs()
        #self.display_inline()

    def solve_most_common_characters(self, data):
        # first, let's find instances where letters double up in the cipher, but only keep one of each letter
        doubles = []
        prev = ''
        for char in self.clean_cipher:
            if prev == char:
                doubles.append(char)
            prev = char

        # now any letter that does not occur naturally (or very rarely) as a double can be excluded as a pair for any doubled letter
        excludes = "ahijkquvwxyz"
        for char in doubles:
            if char in data.alphabet:
                for c in excludes:
                    self.cracked_pairs[char].add_impossible_pair(c)

        a = self.get_words_of_length(1, self.word_by_freq, False)
        # if there is only one word of length 1 it must be 'a' as it's highly unlikely to not have 'a' used at all
        if a.__len__() == 1:
            self.cracked_pairs[a[0]].paired_char = 'a'

        # lets assume the most common letter is an e
        found = False
        for i in range(0, len(self.most_used_char_array)):
            if found:
                pass
            else:
                e = self.most_used_char_array[i]
                self.cracked_pairs[e].paired_char = 'e'
                the = self.encrypt_to_cipher("th")
                the += e
                found_the = self.find_words_with_phrase(self.word_by_freq, the, 3)
                if found_the:
                    self.cracked_pairs[found_the[0][0]].set_paired_char('t')
                    self.cracked_pairs[found_the[0][1]].set_paired_char('h')
                    self.cracked_pairs[e].paired_char = 'e'
                    found = True
        return found


    def fill_unused_chars(self):
        non_paired_chars = []
        s = self.get_result(False)
        for c in self.data.alphabet:
            if c not in s:
                non_paired_chars.append(c)
        for i, char in enumerate(self.unused_letters):
            self.cracked_pairs[char].set_paired_char(non_paired_chars[i])

    def review_substring_patterns(self, cipher_words, word_list):
        for word in cipher_words:
            translation = self.decrypt_from_cipher(word)
            if '?' in translation:
                for _word in word_list:
                    s = self.decrypt_from_cipher(self.encrypt_to_cipher(_word))
                    if s in translation:
                        i = self.get_start_pos_in_string(translation, s)
                        if self.get_amount_of_char_in_word(s, '?') == 1 and self.get_amount_of_char_in_word(translation, '?') == 1:
                            for j, char in enumerate(translation):
                                if char == '?':
                                    self.cracked_pairs[word[j]].set_paired_char(_word[j - i])
                        elif self.get_amount_of_char_in_word(s, '?') == self.get_amount_of_char_in_word(translation, '?'):
                            pass

    def get_start_pos_in_string(self, string, substring):
        if substring in string:
            for i, c in enumerate(string):
                if string[i:i+len(substring)] == substring:
                    return i
        return -1

    def get_unpaired_chars(self):
        alphabet = self.data.letters_by_freq
        used_chars = ""
        unused = ""
        for char in self.cracked_pairs.keys():
            if self.cracked_pairs[char].is_char_paired():
                used_chars += "{}".format(self.cracked_pairs[char].paired_char)
        for char in alphabet:
            if char not in used_chars:
                unused += "{}".format(char)
        return unused

    def get_real_word_possible_matches_for_cipher_word(self,cipher_word, real_words):
        # takes an encrypted word with possible wildcards and returns words it could be
        matches = []
        cipher_word_to_real = self.decrypt_from_cipher(cipher_word)
        for word in real_words:
            translation = self.encrypt_to_cipher(word)
            if self.decrypt_from_cipher(translation) == cipher_word_to_real:
                matches.append(word)
        return matches

    def get_wildcard_indexes(self, word):
        indexes = []
        for i, char in enumerate(word):
            if char == '?':
                indexes.append(i)
        return indexes

    def find_encrypted_wildcard_matches(self, cipher_words, search_term, restrict_to_full_words=True):
        if restrict_to_full_words:
            return self.find_words_with_phrase(cipher_words, search_term, search_term.__len__())
        return self.find_words_with_phrase(cipher_words, search_term)

    def search_for_words_in_cipher(self, cipher_words, search_words, restrict_to_full_words=True):
        # takes words and translates them into the cipher and then searches for them
        # TODO: this needs re writing so we can take words containing the search_term and fill parts of it in
        for word in search_words:
            translation = self.encrypt_to_cipher(word)
            indexes = self.get_wildcard_indexes(translation)
            chars = []
            for i in indexes:
                chars.append(word[i])
            search_results = self.find_encrypted_wildcard_matches(cipher_words, translation, restrict_to_full_words)
            if not restrict_to_full_words:
                print("full words only supported currently")
                exit()
            if search_results:
                if '?' in translation:
                    if self.get_amount_of_char_in_word(translation, '?') == 1:
                        for i, char in enumerate(translation):
                            if char == '?':
                                letter = word[i].lower()
                                chars = ""
                                for _word in search_results:
                                    chars += self.cracked_pairs[_word[i]].paired_char
                                for _word in search_results:
                                    if self.cracked_pairs[_word[i]].paired_char == '?':
                                        if chars.__len__() == 1 or self.get_amount_of_char_in_word(chars, '?') == 1:
                                            self.cracked_pairs[_word[i]].set_paired_char(letter)
                                            self.words_used += 1

    def find_words_in_cypher(self, cipher_words, search_term, is_full_words_only=True):
        #translates the search_term into the cipher, works out which letters have not been deciphered yet and assigns them wildcards
        translation = self.encrypt_to_cipher(search_term)
        wildcard_indexes = []
        for i, char in enumerate(translation):
            if char == '?':
                wildcard_indexes.append(i)
        return self.find_encrypted_wildcard_matches(cipher_words, translation, True)

    def are_all_chars_same(self, char_array):
        if len(char_array) == 0:
            return False
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

    def get_amount_of_char_in_word(self, word, char):
        count = 0
        for c in word:
            if c == char:
                count += 1
        return count


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

    def encrypt_to_cipher(self, word):
        # takes a word and attempts to translate it back into the cypher, an incomplete key/value set for CrackedPairs will return '?'
        s = ""
        for char in word:
            s += self.get_char_representative_in_cipher(char)
        return s

    def decrypt_from_cipher(self, word):
        #takes an encrypted word and attempts to decrpyt it using the crackedpairs, any incomplete decryptions return a '?' in place of translated chars
        s = ""
        for char in word:
            if char != '?':
                try:
                    int(char)  # If there are numbers in the cipher we just ignore them
                except:
                    s += self.cracked_pairs[char].paired_char
            else:
                s += '?'
        return s

    def display_result(self, start_time, preserve_punctuation=True, is_filling_unknowns=False):
        s = "word"
        if self.words_used > 1:
            s += "s"
        f = self.decide_solve_confidence(is_filling_unknowns)
        if f >= 100:
            print("Took {:.3f} seconds to completely solve the cipher, using {} {}".format(
                time.time() - start_time, self.words_used, s))
        else:
            print("Took {:.3f} seconds to solve cipher to a {:.1f}% confidence, interpreting {} {}.".format(time.time() - start_time, f, self.words_used, s))
        print("\n")
        print(self.get_result(preserve_punctuation))

    def get_result(self, preserve_punctuation):
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
        return new_cipher

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
        # size of words returned can be limited by optional parameter size_limit (so we can search chunks of a word)
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

    def decide_solve_confidence(self, is_filling_unknowns):
        total = 0
        solved = 0
        for k in self.cracked_pairs.keys():
            total += 1
            if self.cracked_pairs[k].paired_char != '?':
                solved += 1
        if is_filling_unknowns:
            return ((solved - len(self.unused_letters))/total) * 100
        return (solved/total) * 100

    def display_inline(self):
        s = ""
        for k in self.cracked_pairs.keys():
            s += " {}".format(k)
        print(s)
        s = ""
        for k in self.cracked_pairs.keys():
            s += " |"
        print(s)
        s = ""
        for k in self.cracked_pairs.keys():
            s += " V"
        print(s)
        s = ""
        for k in self.cracked_pairs.keys():
            s += " {}".format(self.cracked_pairs[k].paired_char)
        print(s)

    def display_grid(self, display_side_by_side=False):
        amt_in_column = 5
        columns = []
        columns2 = []
        column = []
        column2 = []
        columns3 = self.get_rep_char_grid()
        for i in range(0, len(self.cracked_pairs.keys())):
            for j, c in enumerate(self.cracked_pairs.keys()):
                if j == i:
                        column.append(self.cracked_pairs[c].paired_char)
                        column2.append(self.cracked_pairs[c].representing_char)
            if i % amt_in_column == 0 and i != 0:
                columns.append(column)
                columns2.append(column2)
                column = []
                column2 = []
        max_len = 0
        for c in columns:
            if len(c) > max_len:
                max_len = len(c)

        for i in range(0, max_len):
            s = ""
            if display_side_by_side:
                for c in columns2:
                    if i >= len(c):
                        s += "   "
                    else:
                        s += " {} ".format(c[i])
            if display_side_by_side:
                if i == (max_len/2) - 1:
                    s += "  ->  "
                else:
                    s += "      "
            for c in columns:
                if i >= len(c):
                    s += "   "
                else:
                    s += " {} ".format(c[i])
            if display_side_by_side:
                if i == (max_len/2) - 1:
                    s += "  ->  "
                else:
                    s += "      "
            for c in columns3:
                if i >= len(c):
                    s += "   "
                else:
                    s += " {} ".format(c[i])
            print(s)


    def get_rep_char_grid(self):
        row_max = 5
        col_max = 6
        columns = []
        used = []
        a = self.data.alphabet
        for x in range(0, row_max):
            column = []
            for y in range(0, col_max):
                for k in self.cracked_pairs.keys():
                    if self.cracked_pairs[k].paired_char == a[(x * row_max) + y]:
                        if k not in used:
                            used.append(k)
                            column.append(k)
            columns.append(column)
        max_len = len(columns[0])
        for i in range(0, max_len):
            s = ""
            for c in columns:
                if len(c) > i:
                    s += " {} ".format(c[i])
        return columns




Decipher("tigcsvqhpi hj qat vchbhqhet gcsvqplcfvahg pvtcfqhpi xjtm qp tijxct jtgctgs pc gpizhmtiqhfohqs pz " +
         "hizpcbfqhpi qcfijbhqqtm fgcpjj fi xijtgxctm gpbbxihgfqhpi gafiito. qat tigcsvqhpi pvtcfqhpi qfutj f vhtgt pz" +
         " hizpcbfqhpi, fojp gfootm btjjflt pc vofhiqtkq, fim qcfijzpcbj hq hiqp f gcsvqplcfb pc ghvatcqtkq xjhil f "+
         "jtgctq gcsvqplcfvahg uts. mtgcsvqhpi hj qat ctetcjt pvtcfqhpi qp tigcsvqhpi. qat ctgthetc dap apomj qat gpcctgq"+
         " jtgctq uts gfi ctgpetc qat btjjflt (vofhiqtkq) zcpb qat gcsvqplcfb (ghvatcqtkq).")

Decipher("gq dtj mxgfvrs cutrgyul qatq qau tjjxbwqgph pz th gehpcthq tqqtfvuc dtj hpq cutrgjqgf. bpjq utcrs uxcpwuth"+
         " fcswqpjsjqubj ducu lujgehul qp dgqajqthl qau tqqtfvj pz ulxftqul pwwphuhqj dap vhud qau uhfcswqgph wcpfujj,"+
         " nxq lgl hpq vhpd qau fcswqpectwagf vus. tllgqgphtrrs, gq dtj cumxujqul qatq qau uhfcswqgph thl lufcswqgph "+
         "wcpfujjuj fpxrl nu lphu mxgfvrs, xjxtrrs ns athl, pc dgqa qau tgl pz bufathgftr luigfuj jxfa "+
         "tj qau fgwauc lgjv ghiuhqul ns ruph ntqqgjt trnucqg.")

Decipher("ij 1976 pizziu cjp bummecj ijsfrpxhup sbu hrjhuws rz wxdmih-vut hftwsrktksuek. wxdmih-vut hftwsrktksuek "+
         "(cmkr hcmmup ckteeusfih ktksuek) xku sgr pizzufujs vutk; rju ik wxdmih gbimu sbu rsbuf ik vuws kuhfus. "+
         "hmucfmt, is ik fuaxifup sbcs hrewxsijo sbu kuhfus vut zfre sbu wxdmih rju bck sr du ijsfchscdmu. ij 1978 "+
         "sbfuu pukiojk dckup rj sbu jrsirj rz wxdmih-vut ktksuek gufu wxdmikbup.")

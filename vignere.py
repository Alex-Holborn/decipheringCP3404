class Vignere:

    def __init__(self, cipher):
        self.cipher = cipher
        self.trigraphs = self.get_trigraphs()
        print(self.cipher)
        self.dists = []
        for t in self.trigraphs.keys():
            if self.trigraphs[t] > 1:
                dist = self.get_distances_between_repeating_trigraph(t)
                for d in dist:
                    if d not in self.dists and d % 2 == 0:
                        self.dists.append(d)
        print("distances : {}".format(self.dists))
        print("common factors: {}".format(self.get_common_factors(self.dists)))
        self.factors = self.get_common_factors(self.dists)
        self.highest_factor = self.get_highest_factor(self.factors)
        self.cipher_lines = self.arrange_cipher_by_highest_factor() # An array of arrays, with cipher formed into words of len(highest factor)
        self.chunks = []
        for line in self.cipher_lines:
            for chunk in line:
                self.chunks.append(chunk)
        self.char_freq = self.get_char_freq_distribution()
        for d in self.char_freq:
            print(d)
        self.analyse_keyword(self.char_freq)
        print(self.recover_plaintext("public")) # Ideally I would like to automatically recover the keyword but it is outside the necessary scope for this assignment

    def get_trigraphs(self):
        # returns all trigraphs (groups of 3 characters) in cipher as keys and amount they appear as values
        trigraphs = {}
        for i in range(0, len(self.cipher)):
            if i + 2 <= len(self.cipher):
                trigraph = self.cipher[i:i+3]
                if trigraph not in trigraphs.keys():
                    trigraphs[trigraph] = 1
                else:
                    trigraphs[trigraph] += 1
        return trigraphs

    def get_indexes_of_repeating_trigraph(self, trigraph):
        # returns the indexes where a repeating trigraph begins
        indexes = []
        for i in range(0, len(self.cipher)):
            if i + 2 <= len(self.cipher):
                if self.cipher[i:i+3] == trigraph:
                    indexes.append(i)
        return indexes

    def get_distances_between_repeating_trigraph(self, trigraph):
        # returns the distances between repeating indexes of a trigraph
        dists = []
        indexes = self.get_indexes_of_repeating_trigraph(trigraph)
        for i, c in enumerate(indexes):
            if i != 0:
                dists.append(indexes[i] - indexes[i-1])
        return dists

    def get_common_factors(self, numbers):
        factors = []
        for i in range(2, 12):
            for n in numbers:
                if n % i == 0:
                    if i not in factors:
                        factors.append(i)
                else:
                    if i in factors:
                        factors.remove(i)
        return factors

    def get_highest_factor(self, factors):
        i = 0
        for f in factors:
            if f > i:
                i = f
        return i

    def arrange_cipher_by_highest_factor(self):
        lines = []
        line = []
        s = ""
        word = ""
        number_per_line = 10
        amt = 0
        for i, c in enumerate(self.cipher):
            word += self.cipher[i]
            if i != 0 and len(word) == self.highest_factor:
                line.append(word)
                s += word
                s += " "
                word = ""
                amt += 1
                if amt == number_per_line:
                    lines.append(line)
                    line = []
                    amt = 0
                    print(s)
                    s = ""
        print(s)
        return lines

    def get_char_freq_distribution(self):
        dicts = [] # we need a dictionary for each letter in the key word
        for i in range(0, self.highest_factor):
            d = {}
            dicts.append(d)
        for word in self.chunks:
            for i in range(0, self.highest_factor):
                if word[i] in dicts[i].keys():
                    dicts[i][word[i]] += 1
                else:
                    dicts[i][word[i]] = 1
        return dicts


    def get_letter_by_letter_steps(self, letter, letter_step):
        # takes a letter and shifts backwards by the value given from character letter_step
        vals = {}
        alph = "abcdefghijklmnopqrstuvwxyz"
        for i, c in enumerate(alph):
            vals[c] = i
        decrement = vals[letter_step]
        val = (vals[letter] - decrement) % len(alph)
        for k in vals.keys():
            if vals[k] == val:
                return k
        return None

    def analyse_keyword(self, dicts):
        for d in dicts:
            greatest = ""
            for k in d.keys():
                if greatest == "":
                    greatest = k
                else:
                    if d[k] > d[greatest]:
                        greatest = k
            print("{} -> {} -> {}".format(greatest, self.get_letter_by_letter_steps(greatest, 'e'), self.get_letter_by_letter_steps(greatest, 't')))

    def recover_plaintext(self, key):
        # at this point words and key are same length so it is just simple iterations
        text = []
        for chunk in self.chunks:
            s = ""
            for i, c in enumerate(chunk):
                s += self.get_letter_by_letter_steps(c, key[i])
            text.append(s)
            s = ""
        t = ""
        for _t in text:
            t += _t
        return t


v = Vignere("pgbuwtelpmtgbcoptgrnszvkruvnbkdhqcwvdwpwakhbphbqelpemeivjolggmgcwopwpczwenbfkvxiopmtpgbwqexivdiwrnjzvgtlntojicoqtwthdpbjtuvnbkdhqcwetyetvihcolucchfcqpriodquiyoeekibusmcjwutwpgompahdlfiioeffepgpodeqqcyfcukvbunpqdmfewdaidvjksmjyaggnglsgqcedavtumaiabyoeargigttgqceomthiqpvutumpldxxtazkdluzbjtqjyvggxfemtbcolbkdhqsiutislecgxusmkiynewudgfzvgdnipzvwuoepgayhtbkbuupekchfcnwgnipzodlfepggynlggmctekqafvdqqcvfeegthusmcjwutwptyslvfhinpwhibfmqfsysdakbcmlzvdmittnxhhtvithfcinpfmdkjtgfdkccvfntchmjqqgsudnwtscorbqwixepgnxfltyxniepkhjszjntgxppckyjompicgtmfibfqwnaixtviilvdbodxfwacjwutwptysezwhnusquxmusmgpmjpavpheepgbitecppwdpxvpvmpaqaoutwpibfepgelpmtgbcoqieinipejdffazqqffxavtgtqzqbqipbjtlusmcjwutwptysswptmuwghdfmzeuibfazqiidztqghpeiuhontviibbebjtuvnbkdhfpzkhuuccuiqpcbjnbphmxtltztxtmnlvagympdccnqcwdayndmihydfzkisbywpngjeggiwusquxmxsgcaffiquicorqpiysymvpodeqqcmjemuuomwgvgotebjtuvnbkdhfpz")
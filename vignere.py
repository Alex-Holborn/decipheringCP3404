class Vignere:

    def __init__(self, cipher):
        self.cipher = cipher
        self.trigraphs = self.get_trigraphs()
        print(self.cipher)
        #print(self.trigraphs)
        self.dists = []
        for t in self.trigraphs.keys():
            if self.trigraphs[t] > 1:
                dist = self.get_distances_between_repeating_trigraph(t)
                for d in dist:
                    if d not in self.dists and d % 2 == 0:
                        self.dists.append(d)
                # print("{} -> {} -> {}".format(t, self.get_indexes_of_repeating_trigraph(t), dist))
        print("distances : {}".format(self.dists))
        self.factors = self.get_common_factors(self.dists)
        self.highest_factor = self.get_highest_factor(self.factors)
        self.arrange_cipher_by_highest_factor()

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
        s = ""
        word = ""
        number_per_line = 10
        amt = 0
        for i, c in enumerate(self.cipher):
            word += self.cipher[i]
            if i != 0 and len(word) == self.highest_factor:
                s += word
                s += " "
                word = ""
                amt += 1
                if amt == number_per_line:
                    amt = 0
                    print(s)
                    s = ""
        print(s)

v = Vignere("pgbuwtelpmtgbcoptgrnszvkruvnbkdhqcwvdwpwakhbphbqelpemeivjolggmgcwopwpczwenbfkvxiopmtpgbwqexivdiwrnjzvgtlntojicoqtwthdpbjtuvnbkdhqcwetyetvihcolucchfcqpriodquiyoeekibusmcjwutwpgompahdlfiioeffepgpodeqqcyfcukvbunpqdmfewdaidvjksmjyaggnglsgqcedavtumaiabyoeargigttgqceomthiqpvutumpldxxtazkdluzbjtqjyvggxfemtbcolbkdhqsiutislecgxusmkiynewudgfzvgdnipzvwuoepgayhtbkbuupekchfcnwgnipzodlfepggynlggmctekqafvdqqcvfeegthusmcjwutwptyslvfhinpwhibfmqfsysdakbcmlzvdmittnxhhtvithfcinpfmdkjtgfdkccvfntchmjqqgsudnwtscorbqwixepgnxfltyxniepkhjszjntgxppckyjompicgtmfibfqwnaixtviilvdbodxfwacjwutwptysezwhnusquxmusmgpmjpavpheepgbitecppwdpxvpvmpaqaoutwpibfepgelpmtgbcoqieinipejdffazqqffxavtgtqzqbqipbjtlusmcjwutwptysswptmuwghdfmzeuibfazqiidztqghpeiuhontviibbebjtuvnbkdhfpzkhuuccuiqpcbjnbphmxtltztxtmnlvagympdccnqcwdayndmihydfzkisbywpngjeggiwusquxmxsgcaffiquicorqpiysymvpodeqqcmjemuuomwgvgotebjtuvnbkdhfpz")
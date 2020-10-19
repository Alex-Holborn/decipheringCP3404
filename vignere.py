class Vignere:

    def __init__(self, cipher):
        self.cipher = cipher
        print(self.get_trigraphs())

    def get_trigraphs(self):
        # returns all trigraphs (groups of 3 characters) in cipher as keys and amount they appear as values
        trigraphs = {}
        for i in range(0, len(self.cipher)):
            if i + 2 <= len(self.cipher):
                trigraph = self.cipher[i:i+3]
                if trigraph not in trigraphs.keys():
                    trigraphs[trigraph] = 0
                else:
                    trigraphs[trigraph] += 1
        return trigraphs

v = Vignere("pgbuwtelpmtgbcoptgrnszvkruvnbkdhqcwvdwpwakhbphbqelpemeivjolggmgcwopwpczwenbfkvxiopmtpgbwqexivdiwrnjzvgtlntojicoqtwthdpbjtuvnbkdhqcwetyetvihcolucchfcqpriodquiyoeekibusmcjwutwpgompahdlfiioeffepgpodeqqcyfcukvbunpqdmfewdaidvjksmjyaggnglsgqcedavtumaiabyoeargigttgqceomthiqpvutumpldxxtazkdluzbjtqjyvggxfemtbcolbkdhqsiutislecgxusmkiynewudgfzvgdnipzvwuoepgayhtbkbuupekchfcnwgnipzodlfepggynlggmctekqafvdqqcvfeegthusmcjwutwptyslvfhinpwhibfmqfsysdakbcmlzvdmittnxhhtvithfcinpfmdkjtgfdkccvfntchmjqqgsudnwtscorbqwixepgnxfltyxniepkhjszjntgxppckyjompicgtmfibfqwnaixtviilvdbodxfwacjwutwptysezwhnusquxmusmgpmjpavpheepgbitecppwdpxvpvmpaqaoutwpibfepgelpmtgbcoqieinipejdffazqqffxavtgtqzqbqipbjtlusmcjwutwptysswptmuwghdfmzeuibfazqiidztqghpeiuhontviibbebjtuvnbkdhfpzkhuuccuiqpcbjnbphmxtltztxtmnlvagympdccnqcwdayndmihydfzkisbywpngjeggiwusquxmxsgcaffiquicorqpiysymvpodeqqcmjemuuomwgvgotebjtuvnbkdhfpz")
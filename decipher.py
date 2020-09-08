class decipher:

    def __init__(self):
        self.cipher = input("Paste Cipher : ")
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.cracked_cipher = ""
        self.letters_by_freq = ['e', 't', 'r', 'i', 'n', 'o', 'a', 's', 'd', 'c', 'h', 'l', 'f', 'u', 'p', 'm', 'y', 'g', 'v', 'w', 'b', 'k', 'q', 'x', 'j', 'z']
        self.punctuation = "./,';:()!?\\ "
        self.ordered_dict = self.order_cipher_by_use()
        ordered_array = self.get_cipher_by_use_to_array(self.ordered_dict)

    def get_cipher(self):
        return self.cipher

    def order_cipher_by_use(self):
        letters = {}
        for words in self.get_cipher():
            for word in words:
                for letter in word:
                    if letter not in letters.keys():
                        if letter not in self.punctuation:
                            letters[letter] = 1
                    else:
                        letters[letter] += 1
        for letter in self.alphabet:
            if letter not in letters.keys():
                letters[letter] = 0
        print(letters)
        return letters

    def get_most_used_letter(self):
        ##returns most used letter in cipher
        most_used = ''
        amt_used = 0
        for k, v in self.ordered_dict.items():
            if v > amt_used:
                most_used = k
                amt_used = v
        return most_used, amt_used

    def get_cipher_by_use_to_array(self, cypher_dict):
        ## returns an array of chars ordered from most used to least used in the cipher
        ordered = []
        for k,v in cypher_dict.items():
            if ordered.__len__() == 0:
                ordered.append(k)
            else:
                for i, letter in enumerate(ordered):
                    if letter != k:
                        if self.get_letter_use_count(letter) > self.get_letter_use_count(k):
                            if i == ordered.__len__() - 1:
                                ordered.append(k)
                        else:
                            ordered.insert(i, k)
                            break
        return ordered


    def get_letter_use_count(self, letter):
        ##returns use count of letter
        return self.ordered_dict[letter]

    def get_duplicate_words(self):
        words = self.get_cipher().split(' ')
        words1 = []
        dupe_words = []

        for word in words:
                if word not in words1:
                    words1.append(word)
                else:
                    if word not in dupe_words:
                        dupe_words.append(word)
        return dupe_words
    


d = decipher()

print("most used: {}".format(d.get_most_used_letter()))
print("duplicated words : {}".format(d.get_duplicate_words()))
print(d.get_cipher_by_use_to_array())

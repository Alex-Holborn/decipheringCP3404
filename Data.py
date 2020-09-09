class Data:

    def __init__(self):
        ##words are ordered by frequency based on an analysis of the Oxford English Corpus
        ##https://en.wikipedia.org/wiki/Most_common_words_in_English
        self.oneLetterWords = ["a", "i"]
        self.twoLetterWords = ["be", "to", "of", "in", "it", "on", "he", "as", "do", "at"]
        self.threeLetterWords = ["the", "and", "for", "not", "you", "but", "his", "say", "her", "she", "who"]
        self.fourLetterWords = ["that", "have", "with", "this", "from", "they", "will", "what"]
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.letters_by_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w',
                                'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']
        self.punctuation = "./,';:()!?\\-+"



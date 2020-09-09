class Data:

    def __init__(self):
        ##words are ordered by frequency based on an analysis of the Oxford English Corpus
        ##https://en.wikipedia.org/wiki/Most_common_words_in_English
        oneLetterWords = ["a", "i"]
        twoLetterWords = ["of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if",
                          "me", "my", "up", "an", "go", "no", "us", "am"]
        threeLetterWords = ["the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "had", "her", "was",
                            "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old",
                            "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"]
        fourLetterWords = ["that", "with", "have", "this", "will", "your", "from", "they", "know", "want", "been",
                           "good", "much", "some", "time", "text"]
        fiveLetterWords = ["attack", "crypt"]

        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.letters_by_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w',
                                'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']
        self.words = []
        self.words.append(oneLetterWords)
        self.words.append(twoLetterWords)
        self.words.append(threeLetterWords)
        self.words.append(fourLetterWords)
        self.words.append(fiveLetterWords)
        self.punctuation = "./,';:()!?\\-+"



class Data:

    def __init__(self):

        twoLetterWords = ["of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if",
                          "me", "my", "up", "an", "go", "no", "us", "am", "qu"]
        threeLetterNouns = ["use", "odd", "boy", "way", "key", "bit"]  # okay, not strictly nouns, but words that can have an s appended
        threeLetterVerbs = ["use", "buy", "add"]   # words that can have -ing or -ed suffix added
        threeLetterWords = ["the", "and", "for", "are", "but", "bet", "bat", "hot", "not", "you", "all", "any", "can", "had", "her", "was",
                            "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old",
                            "see", "two", "who", "did", "let", "put", "say", "she", "too", "off", "end"]
        fourLetterNouns = ["will", "call", "your", "good", "want", "door", "back", "tour", "know", "text", "take", "live", "post", "show"]
        fourLetterVerbs = ["pace", "text", "back", "time", "know", "want", "have", "live", "post", "show", "call"]
        fourLetterWords = ["that", "with", "have", "this", "from", "they", "been", "much", "some", "time", "text",
                           "most", "also", "four", "five", "were", "east", "west", "free", "area", "keep", "kept",
                           "onto", "upon", "when", "then", "them", "over", "here", "both", "pass", "word"]
        fiveLetterNouns = ["attack", "crypt", "place", "piece", "front", "device", "arrear", "design"]
        fiveLetterVerbs = ["attack", "crypt", "place", "piece", "front"]
        fiveLetterWords = ["attack", "crypt", "three", "place", "peace", "piece" "front", "found", "north", "south",
                           "early", "there", "where", "quick", "other", "think", "thank", "thing", "clear", "under"]

        sixPlusLetterWords = ["across", "access", "receive", "recover", "realise", "realize", "public", "private",
                              "object", "within", "without", "require"]
        sixPlusLetterNouns = ["receive", "recover", "realise", "realize", "public", "private", "object", "require"]
        sixPlusLetterVerbs = ["access", "receive", "recover", "realise", "realize", "object", "require"]

        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.letters_by_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w',
                                'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']
        self.words = []
        self.words.append(twoLetterWords)

        self.words.append(threeLetterWords)
        self.words.append(threeLetterNouns)
        self.words.append(threeLetterVerbs)
        self.words.append(self.create_pluralised_words(threeLetterNouns))
        self.words.append(self.create_past_verbs(threeLetterVerbs))
        self.words.append(self.create_present_verbs(threeLetterVerbs))
        self.words.append(self.create_personable_verbs(threeLetterVerbs))

        self.words.append(fourLetterWords)
        self.words.append(fourLetterNouns)
        self.words.append(fourLetterVerbs)
        self.words.append(self.create_pluralised_words(fourLetterNouns))
        self.words.append(self.create_past_verbs(fourLetterVerbs))
        self.words.append(self.create_present_verbs(fourLetterVerbs))
        self.words.append(self.create_personable_verbs(fourLetterVerbs))

        self.words.append(fiveLetterWords)
        self.words.append(fiveLetterNouns)
        self.words.append(self.create_pluralised_words(fiveLetterNouns))
        self.words.append(self.create_past_verbs(fiveLetterVerbs))
        self.words.append(self.create_present_verbs(fiveLetterVerbs))
        self.words.append(self.create_personable_verbs(fiveLetterVerbs))

        self.words.append(sixPlusLetterWords)
        self.words.append(sixPlusLetterVerbs)
        self.words.append(self.create_pluralised_words(sixPlusLetterNouns))
        self.words.append(self.create_past_verbs(sixPlusLetterVerbs))
        self.words.append(self.create_present_verbs(sixPlusLetterVerbs))
        self.words.append(self.create_personable_verbs(sixPlusLetterVerbs))

        self.punctuation = "./,';:()!?\\-+{}"


    def create_pluralised_words(self, word_list):
        words = []
        for word in word_list:
            words.append("{}{}".format(word, 's'))
        return words

    def create_present_verbs(self, word_list):
        words = []
        for word in word_list:
            if word[-1] == 'e':
                word = word[0:word.__len__() - 1]
            words.append("{}{}".format(word, "ing"))
        return words

    def create_past_verbs(self, word_list):
        words = []
        for word in word_list:
            if word[-1] == 'e':
                words.append("{}{}".format(word, 'd'))
            else:
                words.append("{}{}".format(word, 'ed'))
        return words

    def create_personable_verbs(self, word_list):
        words = []
        for word in word_list:
            if word[-1] == 'e':
                words.append("{}{}".format(word, 'r'))
            else:
                words.append("{}{}".format(word, 'er'))
        return words


class CrackedPair:

    def __init__(self, char):
        self.representing_char = char
        self.paired_char = '?'
        self.impossible_pairs = []

    def set_paired_char(self, char):
        self.paired_char = char

    def add_impossible_pair(self, char):
        if char not in self.impossible_pairs and char != self.paired_char:
            self.impossible_pairs.append(char)

    def is_char_paired(self):
        return self.paired_char != '?'

    def get_value_differences(self):
        if self.paired_char == '?':
            return -1
        return self.get_value_of_char(self.representing_char) - self.get_value_of_char(self.paired_char)

    def get_value_of_char(self, char):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for i, c in enumerate(alphabet):
            if c == char:
                return i
        return -1
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

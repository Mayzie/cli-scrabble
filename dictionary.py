class Dictionary():
    def __init__(self, dictionary_file='/usr/share/dict/words'):
        with open(dictionary_file, 'r') as f:
            # Remove all trailing newline characters.
            self.dictionary = [word.rstrip().upper() for word in f.readlines()]

    def check_word(self, word):
        """
        Verifies if a word exists in the dictionary or not.
        """
        return word.upper() in self.dictionary

    def find_words(self, letters):
        """
        Finds valid words given a set of tiles.
        """
        result = []
        sorted_letters = ''.join(sorted(letters)).upper()

        for word in self.dictionary:
            sorted_word = sorted(word)


            last_pos = -1
            for i in range(len(sorted_word)):
                # Check if the index the character exists at is one we haven't looked at before.
                if last_pos >= sorted_letters.find(sorted_word[i], last_pos + 1):
                    break
                if i == len(sorted_word) - 1:
                    result.append(word)

                last_pos = sorted_letters.find(sorted_word[i], last_pos + 1)

        return result

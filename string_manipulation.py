

def reverse_words(text):
    words = text.split()
    words_reversed = [reverse_letters_in_word(w) for w in words]
    return " ".join(words_reversed)


def reverse_letters_in_word(word):
    letters = (c for c in word[::-1] if c != '.')
    return "".join([c if not c != '.' else next(letters) for c in word])

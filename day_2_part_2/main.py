from Levenshtein._levenshtein import distance


def get_words_with_levenshtein_1(words):
    for word_1 in words:
        for word_2 in words:
            if word_1 == word_2:
                continue
            dist = distance(word_1, word_2)
            if dist == 1:
                return word_1, word_2
    raise RuntimeError('No words with levenshtein_1 found')


if __name__ == '__main__':
    total_pairs = 0
    total_triples = 0
    similarity = None
    with open('../day_2_part_1/input.txt', encoding='utf-8') as words:
        words_list = list(words)

    word_1, word_2 = get_words_with_levenshtein_1(words_list)

    same_part = ''
    for letter_1, letter_2 in zip(word_1, word_2):
        if letter_1 == letter_2:
            same_part += letter_1

    print(same_part)

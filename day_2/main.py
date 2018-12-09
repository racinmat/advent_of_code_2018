from Levenshtein._levenshtein import distance


def part_1():
    total_pairs = 0
    total_triples = 0
    with open('input.txt', encoding='utf-8') as words:
        for word in words:
            hist = dict()
            for letter in word:
                if letter in hist:
                    hist[letter] += 1
                else:
                    hist[letter] = 1
            if 2 in hist.values():
                total_pairs += 1
            if 3 in hist.values():
                total_triples += 1
    print(total_pairs, total_triples)
    print(total_pairs * total_triples)


def get_words_with_levenshtein_1(words):
    for word_1 in words:
        for word_2 in words:
            if word_1 == word_2:
                continue
            dist = distance(word_1, word_2)
            if dist == 1:
                return word_1, word_2
    raise RuntimeError('No words with levenshtein_1 found')


def part_2():
    with open('input.txt', encoding='utf-8') as words:
        words_list = list(words)

    word_1, word_2 = get_words_with_levenshtein_1(words_list)

    same_part = ''
    for letter_1, letter_2 in zip(word_1, word_2):
        if letter_1 == letter_2:
            same_part += letter_1

    print(same_part)


if __name__ == '__main__':
    part_1()
    part_2()

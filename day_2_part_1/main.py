if __name__ == '__main__':
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

import numpy as np



def word_overlap(w1, w2):
    key = np.array(5*["r"])
    w1,w2 = (np.asarray(list(w)) for w in (w1,w2))
    key[np.isin(w1, w2)] = "y"
    key[w1 == w2] = "g"
    return "".join(key)


def prune(word, remaining_words, overlap):
    chars = np.asarray(list(word))
    overlap = np.asarray(list(overlap))
    r, y, g = (overlap == c for c in ("r", "y", "g"))
    ly = np.sum(y)
    sy = set(chars[y].tolist())
    sr = set(chars[r].tolist()) - sy - set(chars[g].tolist())

    def valid(w):
        lw = list(w)
        aw = np.asarray(lw)
        green = np.all(aw[g] == chars[g])
        yellow = (ly <= len(sy.intersection(lw))) and not np.any(aw[y] == chars[y])
        red = (len(sr.intersection(lw)) == 0) and not np.any(aw[r] == chars[r])
        return green and yellow and red

    pruned = [w for w in remaining_words if valid(w)]
    return pruned


def find_optimal(word_list):
    n = len(word_list)
    expectation = np.zeros(n, dtype=float)
    keys = np.load("keys.npy")

    for i, w1 in enumerate(word_list):
        distribution = {k:0 for k in keys}
        for w2 in word_list:
            k = word_overlap(w1, w2)
            distribution[k] += 1

        for k in distribution:
            expectation[i] += distribution[k]**2 / n ## n(k) * p(k) = n(k)**2 / n_total

    idx = np.argmin(expectation)
    return word_list[idx]


def generate_guess(guess, word_list, overlap):
    pruned = prune(guess, word_list, overlap)
    new_guess = find_optimal(pruned)
    return new_guess, pruned



if __name__ == '__main__':

    # fin = "/usr/share/dict/british-english"
    # with open(fin, 'r') as file:
    #     words = [line.strip() for line in file]
    # words = [word for word in words if (("'" not in word) and (len(word) == 5))]
    # #unique = [word for word in words if (len(set(list(word))) == len(word))]

    guess = "tares" ## pre-determined
    words = np.load("dictionary.npy")

    while 1 < len(words):
        print(guess, len(words))
        res = input("input result: ")
        guess, words = generate_guess(guess, words, res)

    print(guess, len(words))


#!python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

from data import DICTIONARY, LETTER_SCORES, POUCH
from random import sample
from itertools import permutations

NUM_LETTERS = 7


# re-use from challenge 01
def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


# re-use from challenge 01
def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)

def draw_letters(p=POUCH, n=NUM_LETTERS):
    """Return a random sample of letters"""
    return sample(p, n)  

def input_word(draw):
    """Ask player for a word.
    Validations: 1) only use letters of draw, 2) valid dictionary word"""
    while True:
        word = input('Form a valid word: ').lower()
        try:
            return _validation(word, draw)
        except ValueError as e:
            print(e)
            continue
            
def get_possible_dict_words(letters):
    """"""
    perm = _get_permutations_draw(letters)
    lst = []
    for word in perm:
        word = ''.join(word).lower()
        try:
            if _validation(word):
                lst.append(word)
        except:
            pass
    return lst

def _get_permutations_draw(lst):
    """"""
    lst = ''.join(lst)
    for k in range(1, len(lst)+1):
        yield from list(permutations(lst, k))

def _validation(word, draw=None):
    """"""
    if draw:
        it = iter(sorted(draw))
        letters = sorted(list(word.upper()))
        if not all(c in it for c in letters):
            raise ValueError('{} can not be created from your letters'.format(word))
    if not word in DICTIONARY:
        raise ValueError('{} is not a valid word in the dictionary'.format(word))
    return word

def main():
    draw = draw_letters()
    print('your draw: {}'.format(','.join(draw)))
    word = input_word(draw)
    word_score = calc_word_value(word)
    print('word: {}\nscore: {}'.format(word, word_score))
    all_poss = get_possible_dict_words(draw)
    max_word = max_word_value(all_poss)
    max_score = calc_word_value(max_word)
    print('optimal: {}\nscore: {}'.format(max_word, max_score))
    score = word_score / max_score * 100
    print('your score: {:.2f}\%'.format(score))


if __name__ == "__main__":
    main()

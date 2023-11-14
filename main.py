from grammar import Grammar
from grammar import get_copy_of_grammar


def test_chomsky():
    initial_grammar = Grammar.generate_random_grammar()
    words_step1 = initial_grammar.backtrack_words(7)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False

def read_test_chomsky():
    initial_grammar = Grammar()
    initial_grammar.read_grammar()
    words_step1 = initial_grammar.backtrack_words(8)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False

def default_test_chomsky():
    initial_grammar = Grammar.default_grammar3()
    words_step1 = initial_grammar.backtrack_words(8)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False

def test_cocke_younger_kasami_check():
    grammar = Grammar.generate_random_grammar()
    init = grammar.copy()
    words_step1 = grammar.backtrack_words(5)

    for word in words_step1:
        if (not grammar.cocke_younger_kasami_check(word)):
            print(word)
            grammar.output_grammar()
            init.output_grammar()
            assert False

def read_test_cocke_younger_kasami_check():
    grammar = Grammar()
    grammar.read_grammar()
    words_step1 = grammar.backtrack_words(8)

    for word in words_step1:
        if (not grammar.cocke_younger_kasami_check(word)):
            print(word)
            assert False

def default_test_cocke_younger_kasami_check():
    grammar = Grammar.default_grammar4()

    words_step1 = grammar.backtrack_words(8)

    for word in words_step1:
        if (not grammar.cocke_younger_kasami_check(word)):
            assert False


# read_test_cocke_younger_kasami_check()
# default_test_cocke_younger_kasami_check()
tests = 100
for i in range(0, tests):
    test_chomsky()
print(f'{tests} tests passed')
tests = 100
for i in range(0, tests):
    test_cocke_younger_kasami_check()
print(f'{tests} tests passed')

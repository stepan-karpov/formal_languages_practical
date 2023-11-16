from grammar import Grammar
from grammar import get_copy_of_grammar

def test_default1_chomsky():
    initial_grammar = Grammar.default_grammar1()
    words_step1 = initial_grammar.backtrack_words(7)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    print("test with default grammar1 passed")

def test_default2_chomsky():
    initial_grammar = Grammar.default_grammar2()
    words_step1 = initial_grammar.backtrack_words(7)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    print("test with default grammar2 passed")

def test_default3_chomsky():
    initial_grammar = Grammar.default_grammar3()
    words_step1 = initial_grammar.backtrack_words(7)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    print("test with default grammar3 passed")

def test_default4_chomsky():
    initial_grammar = Grammar.default_grammar4()
    words_step1 = initial_grammar.backtrack_words(7)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    print("test with default grammar4 passed")

def test_default5_chomsky():
    initial_grammar = Grammar.default_grammar5()
    words_step1 = initial_grammar.backtrack_words(7)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    print("test with default grammar5 passed")

def test_cocke_younger_kasami_check():
    grammar = Grammar.generate_random_grammar()
    init = grammar.copy()
    words_step1 = grammar.backtrack_words(5)

    for word in words_step1:
        if (not grammar.cocke_younger_kasami_check(word)):
            assert False

test_default1_chomsky()
test_default2_chomsky()
test_default3_chomsky()
test_default4_chomsky()
test_default5_chomsky()

tests = 1000
for i in range(0, tests):
    test_cocke_younger_kasami_check()
print(f'{tests} tests passed')

from grammar import Grammar
from grammar import get_copy_of_grammar


def test_chomsky():
    global total
    initial_grammar = Grammar.generate_random_grammar()
    words_step1 = initial_grammar.backtrack_words(8)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    words_step2 = grammar_to_change.backtrack_words(3)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    

def read_test_chomsky():
    global total
    initial_grammar = Grammar()
    initial_grammar.read_grammar()
    initial_grammar.output_grammar()
    words_step1 = initial_grammar.backtrack_words(8)
    print(words_step1)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    total += int(grammar_to_change.has_eps())
    assert grammar_to_change.has_eps() == initial_grammar.has_eps()
    grammar_to_change.output_grammar()
    words_step2 = grammar_to_change.backtrack_words(3)
    print(words_step2)
    for word in words_step2:
        if (word not in words_step1):
            assert False
    # assert (words_step1 == words_step2)

def default_test_chomsky():
    initial_grammar = Grammar.default_grammar3()
    words_step1 = initial_grammar.backtrack_words(9)
    print(words_step1)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    grammar_to_change.output_grammar()
    words_step2 = grammar_to_change.backtrack_words(9)
    print(words_step2)

    for word in words_step2:
        if (word not in words_step2):
            assert False


tests = 100
for i in range(0, tests):
    test_chomsky()
print(f'{tests} tests passed')

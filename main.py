from grammar import Grammar
from grammar import get_copy_of_grammar

def test_chomsky():
    initial_grammar = Grammar.generate_random_grammar()

    words_step1 = initial_grammar.backtrack_words()
    # print(words_step1)

    grammar_to_change = get_copy_of_grammar(initial_grammar)
    grammar_to_change.chomsky_do()
    words_step2 = grammar_to_change.backtrack_words()
    # print(words_step2)

    assert (words_step1 == words_step2)
    print("OK!")

for i in range(0, 1000):
    test_chomsky()
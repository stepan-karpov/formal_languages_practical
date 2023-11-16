from grammar import Grammar
from grammar import get_copy_of_grammar

small_words = []

def generate_words(current_word):
    small_words.append(current_word)
    if (len(current_word) == 5):
        return
    for letter in ["a", "b", "c"]:
        generate_words(current_word + letter)

def test_default1_early():
    initial_grammar = Grammar.default_grammar1()
    chomsky_grammar = initial_grammar.copy()
    
    for word in small_words:
        check1 = chomsky_grammar.cocke_younger_kasami_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar1 passed")

def test_default2_early():
    initial_grammar = Grammar.default_grammar2()
    chomsky_grammar = initial_grammar.copy()

    for word in small_words:
        check1 = chomsky_grammar.cocke_younger_kasami_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar2 passed")

def test_default3_early():
    initial_grammar = Grammar.default_grammar3()
    chomsky_grammar = initial_grammar.copy()

    for word in small_words:
        check1 = chomsky_grammar.cocke_younger_kasami_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar3 passed")

def test_default4_early():
    initial_grammar = Grammar.default_grammar4()
    chomsky_grammar = initial_grammar.copy()

    for word in small_words:
        check1 = chomsky_grammar.cocke_younger_kasami_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar4 passed")

def test_default5_early():
    initial_grammar = Grammar.default_grammar5()
    chomsky_grammar = initial_grammar.copy()

    for word in small_words:
        check1 = chomsky_grammar.cocke_younger_kasami_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar5 passed")

def test_early_check():
    initial_grammar = Grammar.generate_random_grammar()
    chomsky_grammar = initial_grammar.copy()
    
    for word in small_words:
        check1 = chomsky_grammar.cocke_younger_kasami_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2

generate_words("")
# print(small_words)
test_default1_early()
test_default2_early()
test_default3_early()
test_default4_early()
test_default5_early()

tests = 1000
for i in range(0, tests):
    test_early_check()
print(f'{tests} tests passed')

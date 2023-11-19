from grammar import Grammar

small_words = []

def generate_words(current_word):
    small_words.append(current_word)
    if (len(current_word) == 5):
        return
    for letter in ["a", "b", "c"]:
        generate_words(current_word + letter)

def test_default1_lr1():
    initial_grammar = Grammar.default_grammar1()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar1 passed")

def test_default1_lr2():
    initial_grammar = Grammar.default_grammar2()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar2 passed")

def test_default1_lr3():
    initial_grammar = Grammar.default_grammar2()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar3 passed")

def test_default1_lr4():
    initial_grammar = Grammar.default_grammar4()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar4 passed")

def test_default1_lr5():
    initial_grammar = Grammar.default_grammar5()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar5 passed")

def test_default1_lr6():
    initial_grammar = Grammar.default_grammar6()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar6 passed")

def test_default1_lr7():
    initial_grammar = Grammar.default_grammar7()    

    for word in small_words:
        check1 = initial_grammar.lr1_check(word)
        check2 = initial_grammar.early_check(word)
        assert check1 == check2
    print("test with default grammar7 passed")

def test_lr1_check():
    grammar = Grammar.generate_random_grammar()
    grammar.output_grammar()
    for word in small_words:
        check1 = grammar.lr1_check(word)
        check2 = grammar.early_check(word)
        # print(word)
        assert check1 == check2

def read_test_lr1_check():
    grammar = Grammar()
    grammar.read_grammar()

    print(grammar.lr1_check("bbccc"))
    

    for word in small_words:
        check1 = grammar.lr1_check(word)
        check2 = grammar.early_check(word)
        print(word)
        assert check1 == check2

generate_words("")

test_default1_lr1()
test_default1_lr2()
test_default1_lr3()
test_default1_lr4()
test_default1_lr5()
test_default1_lr6()
test_default1_lr7()

print("7 tests passed")


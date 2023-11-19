from grammar import Grammar

if __name__ == "__main__":
    grammar = Grammar()
    print("input your grammar and a word in the right format:")
    grammar.read_grammar()
    word = input()
    print()
    print("Can this word be rocognized by this grammar?")
    print("Cocke-Younger-Kasami verdict:\t", grammar.cocke_younger_kasami_check(word))
    print("Early verdict:\t\t\t", grammar.early_check(word))
    print("LR1 verdict:\t\t\t", grammar.lr1_check(word))
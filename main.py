from grammar import Grammar



new_grammar = Grammar.default_grammar2()
new_grammar.output_grammar()

print(new_grammar.backtrack_words()[:30])
### Formal languages and translations - Practical Work No. 2

This repository contains the implementation of a practical assignment. Specifically, it comprises the following:

* Cock-Younger-Kasami algorithm
* Early algorithm
* LR(1) algorithm (to be completed)

Here is a description of files in this repository:

#### [grammar.py](grammar.py)

This file includes the ```Grammar``` class, which implements algorithms. To use it, simply call ```my_grammar = Grammar()``` to create Grammar instance. You can input your grammar by calling ```my_grammar.read_grammar()```. The grammar input format is described in [grammar_examples.txt](grammar_examples.txt). Here is a brief description: the first line should input the start non-terminal symbol, followed by a line containing all non-terminal symbols, then input all terminal symbols, and finally, include all rules separated by ```,```. 

**Important Note**: ```Grammar``` class only supports context-free grammars! If your input contains anything other than this, the behavior is undefined.

#### [chomsky_tests.py](chomsky_tests.py)

This file includes tests for the ```Grammar``` class. There is a check for 1000 random grammars for chomksy normal form and Cock-Younger-Kasami algorithm. To understand which words can be deduced in our grammar, we simply use backtracking with depth specified in the brackets (you can see it in the functions). When we have list of these words, we initiate chomsky normal form algorithm and check if the recognition of each words stays the same with Cock-Younger-Kasami algorithm.

All you have to to do run tests is simply run [chomsky_tests.py](chomsky_tests.py)

#### [early_tests.py](early_tests.py)

This file includes tests for the ```Grammar``` class. There is a check for 1000 random grammars for Early algorithm. Since we've already checked correctness of Cock-Younger-Kasami algorithm, run both Early and Cock-Younger-Kasami algorithms on small word (with length <= 5) and the test will be passed if recognition stays the same

All you have to to do run tests is simply run [early_tests.py](early_tests.py)

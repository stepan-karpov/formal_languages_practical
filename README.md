### Formal languages and translations - Practical Work No. 2

This repository contains the implementation of a practical assignment. Specifically, it comprises the following:

* Cocke-Younger-Kasami algorithm
* Early algorithm
* LR(1) algorithm (to be completed)

Here is a description of files in this repository:

#### [main.py](main.py)

If you're lazy enough to read README.md down below, run this python script and it will show you results of LR1, Early and Cocke-Younger-Kasami algorithms for recognition of the word you input. Don't forget to follow format! Here is an example of input for main.py:
```
S
S A B C
a b c
S->a, S->b, S->c
abcd
```

#### [grammar.py](grammar.py)

This file includes the ```Grammar``` class, which implements algorithms. To use it, simply call ```my_grammar = Grammar()``` to create Grammar instance. You can input your grammar by calling ```my_grammar.read_grammar()```. The grammar input format is described in [grammar_examples.txt](grammar_examples.txt). Here is a brief description: the first line should input the start non-terminal symbol, followed by a line containing all non-terminal symbols, then input all terminal symbols, and finally, include all rules separated by ```,```. 

**Important Note**: ```Grammar``` class only supports context-free grammars! If your input contains anything other than this, the behavior is undefined.

#### [chomsky_tests.py](chomsky_tests.py)

This file includes tests for the ```Grammar``` class. There is a check for 1000 random grammars for chomksy normal form and Cocke-Younger-Kasami algorithm. To understand which words can be deduced in our grammar, we simply use backtracking with depth specified in the brackets (you can see it in the functions). When we have list of these words, we initiate chomsky normal form algorithm and check if the recognition of each words stays the same with Cocke-Younger-Kasami algorithm.

All you have to to do run tests is simply run [chomsky_tests.py](chomsky_tests.py)

#### [early_tests.py](early_tests.py)

This file includes tests for the ```Grammar``` class. There is a check for 1000 random grammars for Early algorithm. Since we've already checked correctness of Cocke-Younger-Kasami algorithm, run both Early and Cocke-Younger-Kasami algorithms on small word (with length <= 5) and the test will be passed if recognition stays the same

All you have to to do run tests is simply run [early_tests.py](early_tests.py)

#### [lr1_tests.py](lr1_tests.py)

This file includes tests for the ```Grammar``` class. There is a check for 7 random grammars for LR1 recognition algorithm. Since we've already checked correctness of Early algorithm, run both Early and LR1 algorithms on small word (with length <= 5) and the test will be passed if recognition stays the same

All you have to to do run tests is simply run [lr1_tests.py](lr1_tests.py)


#### Testing

to test this framework, run ```coverage run -m pytest chomsky_tests.py early_tests.py lr1_tests.py``` and ```coverage report -m >> coverage.txt``` and you'll see testing information
### Formal languages and translations - Practical Work No. 2

This repository contains the implementation of a practical assignment. Specifically, it comprises the following:

* Cock-Younger-Kasami algorithm
* Early algorithm (to be completed)
* LR(1) algorithm (to be completed)

Here is a description of files in this repository:

#### [grammar.py](grammar.py)

This file includes the ```Grammar``` class, which implements algorithms. To use it, simply call ```my_grammar = Grammar()``` to create Grammar instance. You can input your grammar by calling ```my_grammar.read_grammar()```. The grammar input format is described in [grammar_examples.txt](grammar_examples.txt). Here is a brief description: the first line should input the start non-terminal symbol, followed by a line containing all non-terminal symbols, then input all terminal symbols, and finally, include all rules separated by ```,```. 

**Important Note**: ```Grammar``` class only supports context-free grammars! If your input contains anything other than this, the behavior is undefined.


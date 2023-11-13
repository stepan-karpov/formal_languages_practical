from constants import *
import random

def shuffle_string(input_string: str) -> list:
    char_list = list(input_string)
    random.shuffle(char_list)
    return char_list

class Grammar:
  def __init__(self, non_terminals=[], terminals=[], rules=[], start_terminal="S"):
    """ terminals, non_terminals, start terminal is always S """
    self.non_terminals = non_terminals
    self.terminals = terminals
    self.rules = rules
    self.start_terminal = start_terminal
    self.found_words = set()

  def read_grammar(self):
    self.start_terminal = input()
    self.non_terminals = input().split()
    self.terminals = input().split()
    self.rules = [tuple(x[:-1].split("->")) for x in (input() + ",").split()]
    if (self.start_terminal not in self.non_terminals):
      self.non_terminals.append(self.start_terminal)

  def output_grammar(self):
    print("=========== Grammar info: =============", end='\n')
    print("start terminal: ", self.start_terminal)
    print("non_terminals: ", self.non_terminals)
    print("terminals: ", self.terminals)
    print("rules: ", end="")
    for i, rule in enumerate(self.rules):
      if (rule[1] != ""):
        print(f'{rule[0]}->{rule[1]}', end=', ' * int(i != len(self.rules) - 1))
      else:
        print(f'{rule[0]}->""', end=', ' * int(i != len(self.rules) - 1))
    print('\n\n')

  @staticmethod
  def generate_random_grammar():
    start_terminal = "S"
    non_terminals = list(CAPS_ALPHABET[:random.randint(2, 3)])
    non_terminals.append(start_terminal)
    terminals = list(ALPHABET[:random.randint(3, 5)])
    rules = []
    rules.append((
      "S",
      ''.join(random.choice(non_terminals + terminals) for _ in range(random.randint(1, 3)))
    ))
    for i in range(0, random.randint(3, 7)):
      rules.append((
        non_terminals[random.randint(0, len(non_terminals) - 1)],
        ''.join(random.choice(non_terminals + terminals) for _ in range(random.randint(1, 3)))
      ))
    return Grammar(non_terminals, terminals, rules, start_terminal)
    
  def non_terminal_free(self, word: str):
    for non_terminal in self.non_terminals:
      if (non_terminal in word):
        return False
    return True

  def backtrack(self, current_word, depth):
    if (self.non_terminal_free(current_word)):
      self.found_words.add(current_word)
      return
    if (depth > 100):
      return

    for i in range(0, len(current_word)):
      for j in range(i, len(current_word)):
        for rule in self.rules:
          if (rule[0] == current_word[i:j + 1]):
            self.backtrack(current_word[0:i] + rule[1] + current_word[j + 1:], depth + 1)

  def backtrack_words(self):
    if (len(self.found_words) > 0):
      return self.found_words
    self.backtrack("S", 0)
    self.found_words = sorted(list(self.found_words), key=len)
    return self.found_words

  @staticmethod
  def default_grammar1():
    start_terminal = "S"
    non_terminals = ["S"]
    terminals = ["a", "b", "c"]
    rules = [("S", "a"), ("S", "b"), ("S", "c")]
    return Grammar(non_terminals, terminals, rules, start_terminal)

  @staticmethod
  def default_grammar2():
    start_terminal = "S"
    non_terminals = ["S", "T"]
    terminals = ["a", "b"]
    rules = [("S", "T"), ("S", "bT"), ("T", "aTb"), ("T", "")]
    return Grammar(non_terminals, terminals, rules, start_terminal)
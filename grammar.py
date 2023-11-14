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
    self.used = set()

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
    non_terminals = list(CAPS_ALPHABET[:random.randint(1, 4)])
    non_terminals.append(start_terminal)
    terminals = list(ALPHABET[:random.randint(3, 5)])
    rules = []
    rules.append((
      "S",
      ''.join(random.choice(non_terminals + terminals) for _ in range(random.randint(1, 3)))
    ))
    for i in range(0, random.randint(3, 5)):
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
    if (current_word in self.used):
      return
    self.used.add(current_word)

    if (self.non_terminal_free(current_word)):
      self.found_words.add(current_word)
      return

    if (len(current_word) > 50):
      return
    if (depth > 5):
      return

    for i in range(0, len(current_word)):
      for j in range(i, len(current_word)):
        for rule in self.rules:
          if (rule[0] == current_word[i:j + 1]):
            self.backtrack(current_word[0:i] + rule[1] + current_word[j + 1:], depth + 1)

  def backtrack_words(self):
    self.used = set()
    self.backtrack("S", 0)
    self.found_words = sorted(list(self.found_words), key=len)
    return self.found_words

  def delete_not_generative(self):
    deleted = set()
    has_roots = set()
    rules_non_terminal = []
    for rule in self.rules:
      rule_0 = ''.join(char for char in rule[0] if char.isupper())
      rule_1 = ''.join(char for char in rule[1] if char.isupper())

      rules_non_terminal.append([rule_0, rule_1])
      if (rule_1 == ""):
        deleted.add(rule_0)
        has_roots.add(rule_0)

    # deleted - all not generative elements
    # rules_non_terminal - rules without terminal symbols
    can_delete = False
    for deleted_term in deleted:
      while [deleted_term, ""] in rules_non_terminal:
        can_delete = True
        rules_non_terminal.remove([deleted_term, ""])

    while (can_delete):
      can_delete = False

      new_delete = set()
      for i, rule in enumerate(rules_non_terminal):
        rule_1 = ''.join(char for char in rule[1] if char not in deleted)
        rules_non_terminal[i][1] = rule_1
        if (rule_1 == ""):
          can_delete = True
          new_delete.add(rule[0])
          has_roots.add(rule[0])
          can_delete = False

      deleted = new_delete
      for deleted_term in deleted:
        while [deleted_term, ""] in rules_non_terminal:
          can_delete = True
          rules_non_terminal.remove([deleted_term, ""])

    new_rules = []
    for i, rule in enumerate(self.rules):
      ok = True
      for letter in rule[0] + rule[1]:
        if (not (letter.islower() or letter in has_roots)):
          ok = False
          break
      if (ok):
        new_rules.append(rule)
    new_non_terminals = []
    for non_terminal in self.non_terminals:
      if (non_terminal in has_roots):
        new_non_terminals.append(non_terminal)

    if ("S" not in new_non_terminals):
      new_non_terminals.append("S")
    self.non_terminals = new_non_terminals
    self.rules = new_rules

  def delete_unreachable(self):
    used = set("S")
    rules_non_terminal = []
    for rule in self.rules:
      rule_0 = ''.join(char for char in rule[0] if char.isupper())
      rule_1 = ''.join(char for char in rule[1] if char.isupper())
      rules_non_terminal.append([rule_0, rule_1])
    
    modified = False
    for rule in rules_non_terminal:
      if (rule[0] in used):
        for non_terminal in rule[1]:
          if (non_terminal not in used):
            modified = True
            used.add(non_terminal)

    while modified:
      modified = False
      for rule in rules_non_terminal:
        if (rule[0] in used):
          for non_terminal in rule[1]:
            if (non_terminal not in used):
              modified = True
              used.add(non_terminal)

    new_non_terminals = []
    for non_terminal in self.non_terminals:
      if (non_terminal in used):
        new_non_terminals.append(non_terminal)
    self.non_terminals = new_non_terminals

    new_rules = []
    for i, rule in enumerate(self.rules):
      ok = True
      for letter in rule[0] + rule[1]:
        if (not(letter.islower() or letter in used)):
          ok = False
          break
      if (ok):
        new_rules.append(rule)
    self.rules = new_rules
    
  def homskyyi_do(self):
    self.delete_not_generative()
    self.delete_unreachable()

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

  @staticmethod
  def default_grammar3():
    start_terminal = "S"
    non_terminals = ["S", "F", "G"]
    terminals = ["a", "b"]
    rules = [("S", "aFbF"), ("F", "aFb"), ("F", ""), ("F", "Ga"), ("G", "bSG")]
    return Grammar(non_terminals, terminals, rules, start_terminal)

  @staticmethod
  def default_grammar4():
    start_terminal = "S"
    non_terminals = ["S", "A", "B", "C"]
    terminals = ["a", "b"]
    rules = [("S", "aA"), ("A", "a"), ("B", "b")]
    return Grammar(non_terminals, terminals, rules, start_terminal)
  
def get_copy_of_grammar(grammar: Grammar):
  copy = grammar
  copy.found_words = set()
  copy.used = set()
  return copy
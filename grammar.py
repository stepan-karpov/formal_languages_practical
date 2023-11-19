from constants import *
import random

class Grammar:
  def __init__(self, non_terminals=[], terminals=[], rules=[], start_terminal="S"):
    """ terminals, non_terminals, start terminal is always S """
    self.non_terminals = non_terminals
    self.terminals = terminals
    self.rules = rules
    self.start_terminal = start_terminal
    self.found_words = set()
    self.used = set()
    self.in_normal_form = False
    self.isLR1 = True

  def copy(self):
    non_terminals = self.non_terminals.copy()
    terminals =  self.terminals.copy()
    rules =  self.rules.copy()
    start_terminal =  self.start_terminal
    return Grammar(non_terminals, terminals, rules, start_terminal)

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
    temp = self.rules.copy()
    temp.sort()
    for i, rule in enumerate(temp):
      if (rule[1] != ""):
        print(f'{rule[0]}->{rule[1]}', end=', ' * int(i != len(temp) - 1))
      else:
        print(f'{rule[0]}->""', end=', ' * int(i != len(temp) - 1))
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
        ''.join(random.choice(non_terminals + terminals) for _ in range(random.randint(0, 3)))
      ))
    return Grammar(non_terminals, terminals, rules, start_terminal)
    
  def non_terminal_free(self, word: str):
    for non_terminal in self.non_terminals:
      if (non_terminal in word):
        return False
    return True

  def backtrack(self, current_word, depth, final_depth):
    if (current_word in self.used):
      return
    self.used.add(current_word)

    if (self.non_terminal_free(current_word)):
      self.found_words.add(current_word)
      return

    if (len(current_word) > 20):
      return
    if (depth > final_depth):
      return

    for i in range(0, len(current_word)):
      for j in range(i, len(current_word)):
        for rule in self.rules:
          if (rule[0] == current_word[i:j + 1]):
            self.backtrack(current_word[0:i] + rule[1] + current_word[j + 1:], depth + 1, final_depth)

  def backtrack_words(self, depth=5):
    self.used = set()
    self.backtrack(self.start_terminal, 0, depth)
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

    if (self.start_terminal not in new_non_terminals):
      new_non_terminals.append(self.start_terminal)
    self.non_terminals = new_non_terminals
    self.rules = new_rules

  def delete_unreachable(self):
    used = set(self.start_terminal)
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
    
  def clear_useless_letters(self):
    new_non_terminals = []
    rules_concat = ''.join([''.join(rule) for rule in self.rules])
    for non_terminal in self.non_terminals:
      if (non_terminal in rules_concat):
        new_non_terminals.append(non_terminal)
    if (self.start_terminal not in new_non_terminals):
      new_non_terminals.append(self.start_terminal)
    self.non_terminals = new_non_terminals
    
    new_terminals = []
    for terminal in self.terminals:
      if (terminal in rules_concat):
        new_terminals.append(terminal)
    self.terminals = new_terminals

  def delete_mixed(self):
    p = 0
    for terminal in self.terminals:
      while (CAPS_ALPHABET[p] in self.non_terminals):
        p += 1
      letter = CAPS_ALPHABET[p]
      for i, rule in enumerate(self.rules):
        self.rules[i] = (rule[0], rule[1].replace(terminal, letter))
      self.rules.append((letter, terminal))
      self.non_terminals.append(letter)
      p += 1

  def delete_long_rules(self):
    new_rules = []
    unused_non_terminals = []
    for letter in CAPS_ALPHABET:
      if (letter not in self.non_terminals):
        unused_non_terminals.append(letter)

    for rule in self.rules:
      current_root = rule[0]
      current_word = rule[1]
      while (len(current_word) > 2):
        new_rules.append((current_root, current_word[0] + unused_non_terminals[0]))
        current_word = current_word[1:]
        current_root = unused_non_terminals[0]
        self.non_terminals.append(unused_non_terminals[0])
        unused_non_terminals.pop(0)
      new_rules.append((current_root, current_word))
    self.rules = new_rules

  def has_eps(self):
    deleted = set()
    has_eps = set()
    rules_cropped = []
    for rule in self.rules:
      if (rule[1].isupper):
        rules_cropped.append([rule[0], rule[1]])
      if (rule[1] == ""):
        deleted.add(rule[0])
        has_eps.add(rule[0])
    
    can_delete = False
    for deleted_term in deleted:
      while [deleted_term, ""] in rules_cropped:
        can_delete = True
        rules_cropped.remove([deleted_term, ""])

    while (can_delete):
      can_delete = False
      new_delete = set()
      for i, rule in enumerate(rules_cropped):
        rule_1 = ''.join(char for char in rule[1] if char not in deleted)
        rules_cropped[i][1] = rule_1
        if (rule_1 == ""):
          can_delete = True
          new_delete.add(rule[0])
          has_eps.add(rule[0])
          can_delete = False

      deleted = new_delete
      for deleted_term in deleted:
        while [deleted_term, ""] in rules_cropped:
          can_delete = True
          rules_cropped.remove([deleted_term, ""])
    return self.start_terminal in has_eps

  def delete_eps(self):
    new_rules = []
    queue = []
    used = set()
    for rule in self.rules:
      if (rule[1] == ""):
        queue.append(rule[0])
        used.add(rule[0])
      else:
        new_rules.append(rule)
    self.rules = new_rules

    while (len(queue) > 0):
      to_delete_current = queue[0]
      queue.pop(0)
      new_rules = []
      for i, rule in enumerate(self.rules):
        if (to_delete_current not in rule[1]):
          new_rules.append(rule)
          continue
        new_rules.append(rule)
        if (rule[1] == to_delete_current + to_delete_current):
          if (rule[0] not in used):
            queue.append(rule[0])
            used.add(rule[0])
          new_rules.append((rule[0], to_delete_current))
          continue
        right_rule = rule[1].replace(to_delete_current, "")
        if (right_rule == "" and rule[0] not in used):
          queue.append(rule[0])
          used.add(rule[0])
        else:
          if (right_rule != ""):
            new_rules.append((rule[0], right_rule))
      self.rules = new_rules

  def restore_eps(self, has_eps: bool):
    if (has_eps):
      self.rules.append((self.start_terminal, ""))

  def find_endpoints(self, vertex: str):
    ans = []
    for rule in self.rules:
      if (rule[0] != vertex or rule[1] == ""):
        continue
      if ((rule[1].isupper() and len(rule[1]) == 2) or rule[1].islower()):
        ans.append(rule[1])
    return ans

  def chomsky_make_closure(self, current_start: str):
    temp = self.rules.copy()
    self.used_closure[current_start] = 1

    to_remove = []
    to_add = []
    for rule in temp:
      if (rule[0] == current_start and rule[1] != "" and
          rule[1].isupper() and len(rule[1]) != 2):
        if (self.used_closure[rule[1]] == 0):
          self.chomsky_make_closure(rule[1])
        togo = self.find_endpoints(rule[1])
        for vertex in togo:
          to_add.append((rule[0], vertex))
        to_remove.append(rule)
    
    for rule in to_remove:
      while (rule in self.rules):
        self.rules.remove(rule)

    for rule in to_add:
     if (rule not in self.rules):
        self.rules.append(rule)
    
    self.used_closure[current_start] = 1

  def dfs_cycle(self, non_terminal: str):
    self.used_cycle[non_terminal] = 1

    for rule in self.rules:
      if (rule[0] != non_terminal):
        continue
      if (len(rule[1]) == 2 or rule[1].islower()):
        continue
      if (rule[1] == ""):
        continue
      self.parents[rule[1]] = non_terminal

      if (self.used_cycle[rule[1]] == 1):
        return non_terminal
      elif (self.used_cycle[rule[1]] == 0):
        temp_ans = self.dfs_cycle(rule[1])
        if (temp_ans != None):
          return temp_ans
    self.used_cycle[non_terminal] = 2
    return None

  def has_cycle(self):
    self.used_cycle = {}
    self.parents = {}
    for non_terminal in self.non_terminals:
      self.used_cycle[non_terminal] = 0
    ans = None
    for non_terminal in self.non_terminals:
      ans = self.dfs_cycle(non_terminal)
      if (ans != None):
        break 

    if (ans == None):
      return False
    
    cycle = set(ans)
    current_vertex = self.parents[ans]
    while (current_vertex != ans):
      cycle.add(current_vertex)
      current_vertex = self.parents[current_vertex]
    
    new_name = CAPS_ALPHABET[0]
    for i in range(1, len(CAPS_ALPHABET)):
      if (new_name in self.non_terminals):
        new_name = CAPS_ALPHABET[i]

    if (self.start_terminal in cycle):
      new_name = self.start_terminal

    new_rules = []
    for rule in self.rules:
      new_rule = rule
      for non_terminal in cycle:
        new_rule = (
          new_rule[0].replace(non_terminal, new_name),
          new_rule[1].replace(non_terminal, new_name)
        )
      new_rules.append(new_rule)

    new_non_terminals = [new_name]

    for non_terminal in self.non_terminals:
      if (non_terminal not in cycle):
        new_non_terminals.append(non_terminal)
    self.non_terminals = new_non_terminals
    
    self.rules = new_rules
    self.remove_conflicts()
    return True

  def transitive_closure(self):
    found = self.has_cycle()
    while (found):
      found = self.has_cycle()

    self.used_closure = {}
    for non_terminal in self.non_terminals:
      self.used_closure[non_terminal] = 0

    for non_terminal in self.non_terminals:
      self.chomsky_make_closure(non_terminal)

  def remove_conflicts(self):
    for non_terminal in self.non_terminals:
      if ((non_terminal, non_terminal) in self.rules): 
        self.rules.remove((non_terminal, non_terminal))
    self.rules = list(set(self.rules))
    new_rules = []
    for rule in self.rules:
      if (rule[0] != rule[1]):
        new_rules.append(rule)
    self.rules = new_rules

  def chomsky_do(self):
    self.remove_conflicts()
    has_eps = self.has_eps()
    self.delete_not_generative()
    self.delete_unreachable()
    self.clear_useless_letters()
    self.delete_mixed()
    self.delete_long_rules()
    self.remove_conflicts()
    self.delete_eps()
    self.restore_eps(has_eps)
    self.remove_conflicts()
    self.transitive_closure()
    self.in_normal_form = True
    self.remove_conflicts()

  def cocke_younger_kasami_check(self, word):
    if (not self.in_normal_form):
      self.chomsky_do()
    if (word == ""):
      return (self.start_terminal, "") in self.rules
    n = len(word)
    N = len(self.non_terminals)
    dp = [[[False for _ in range(n + 1)] for _ in range(n + 1)] for _ in range(N)]

    pos = {}
    time = 0
    for non_terminal in self.non_terminals:
      pos[non_terminal] = time
      time += 1

    if ((self.start_terminal, "") in self.rules):
      for i in range(0, n + 1):
        dp[pos[self.start_terminal]][i][i] = True

    for i in range(0, n):
      for non_terminal in self.non_terminals:
        dp[pos[non_terminal]][i][i + 1] = (non_terminal, word[i]) in self.rules
    
    for m in range(2, n + 1):
      for i in range(0, n - m + 1):
        j = i + m
        for rule in self.rules:
          A = pos[rule[0]]
          if (rule[1].islower() or rule[1] == "" or dp[A][i][j]):
            continue
          B = pos[rule[1][0]]
          C = pos[rule[1][1]]
          for k in range(i, j + 1):
            dp[A][i][j] = dp[A][i][j] or (dp[B][i][k] and dp[C][k][j])
            if (dp[A][i][j]):
              break
    
    return dp[pos[self.start_terminal]][0][n]

  def calc_rules_from_terminal(self):
    self.rules_from_terminal = {}
    for non_terminal in self.non_terminals:
      self.rules_from_terminal[non_terminal] = []

    for rule in self.rules:
      self.rules_from_terminal[rule[0]].append(rule[1])

  def early_predict(self, situations, j):
    to_adds = []
    for situation in situations[j]:
      from_pos = situation[0]
      to_pos = situation[1]
      ind_pos = situation[2]
      dot_index = to_pos.index(".")
      if (dot_index != len(to_pos) - 1 and to_pos[dot_index + 1].isupper()):
        next_source = to_pos[dot_index + 1]
        for rule in self.rules_from_terminal[next_source]:
          to_adds.append((next_source, "." + rule, j))
    added = False
    for to_add in to_adds:
      if (to_add not in situations[j]):
        situations[j].append(to_add)
        added = True
    return added
  
  def early_scan(self, situations, j, word):
    to_adds = []
    for situation in situations[j]:
      from_pos = situation[0]
      to_pos = situation[1]
      ind_pos = situation[2]
      dot_index = to_pos.index(".")
      if (dot_index != len(to_pos) - 1 and to_pos[dot_index + 1].islower()):
        if (to_pos[dot_index + 1] == word[j]):
          to_adds.append((from_pos, to_pos[:dot_index] + to_pos[dot_index + 1] + "." + to_pos[dot_index + 2:], ind_pos))
    for to_add in to_adds:
      if (to_add not in situations[j + 1]):
        situations[j + 1].append(to_add)
  
  def early_find_sources(self, situations, k, non_terminal):
    answer = []
    for situation in situations[k]:
      to_pos = situation[1]
      dot_index = to_pos.index(".")
      if (dot_index != len(to_pos) - 1 and to_pos[dot_index + 1] == non_terminal):
        answer.append(situation)
    return answer

  def early_complete(self, situations, j):
    to_adds = []
    for situation in situations[j]:
      from_pos = situation[0]
      to_pos = situation[1]
      ind_pos = situation[2]
      if (to_pos.index(".") != len(to_pos) - 1):
        continue
      for source in self.early_find_sources(situations, ind_pos, from_pos):
        dot_index = source[1].index(".")
        to_adds.append((source[0], source[1][:dot_index]
                        + source[1][dot_index + 1] + "."
                        + source[1][dot_index + 2:], source[2]))
    added = False
    for to_add in to_adds:
      if (to_add not in situations[j]):
        situations[j].append(to_add)
        added = True
    return added

  def early_iteration(self, situations, i):
    changes = self.early_complete(situations, i)
    changes |= self.early_predict(situations, i)
    while (changes):
      changes = self.early_complete(situations, i)
      changes |= self.early_predict(situations, i)

  def early_check(self, word):
    if (word == ""):
      return self.has_eps()
    # 0 is analogy of S' in handwritten rules
    self.rules.append(("0", "S"))
    self.non_terminals.append("0")

    self.calc_rules_from_terminal()
    
    situations = [[] for _ in range(len(word) + 1)]

    situations[0].append(("0", ".S", 0))

    self.early_iteration(situations, 0)
    for i in range(1, len(word) + 1):
      self.early_scan(situations, i - 1, word)
      self.early_iteration(situations, i)

    self.rules.remove(("0", "S"))
    self.non_terminals.remove("0")
    return ("0", "S.", 0) in situations[-1]

  def lr1_precalc_first_dfs(self, non_terminal):
    if (non_terminal in self.first.keys()):
      return self.first[non_terminal]
    
    self.first[non_terminal] = []
    for rule in self.rules:
      if (rule[0] == non_terminal):
        if (len(rule[1]) == 0):
          self.first[non_terminal].append("$")
        else:
          self.first[non_terminal].extend(self.lr1_precalc_first_dfs(rule[1][0]))
    return self.first[non_terminal]

  def lr1_first_precalc(self):
    self.first = {"": "$", "$": "$"}
    for terminal in self.terminals:
      self.first[terminal] = [terminal]

    for non_terminal in self.non_terminals:
      self.lr1_precalc_first_dfs(non_terminal)

  def lr1_get_first_from_word(self, word):
    for letter in word:
      if (self.first[letter] != []):
        return self.first[letter]
    return ["$"]

  def lr1_closure(self, vertex):
    new_vertex = vertex
    for rule in vertex:
      to_pos = rule[1]
      first_pos = rule[2]
      dot_pos = to_pos.index(".")
      if (dot_pos != len(to_pos) - 1 and to_pos[dot_pos + 1].isupper()):
        new_start = to_pos[dot_pos + 1]
        next_firsts = self.lr1_get_first_from_word(to_pos[dot_pos + 2:] + first_pos)
        for from_rule in self.rules_from_terminal[new_start]:
          for next_first in next_firsts:
            new_value = (new_start, "." + from_rule, next_first)
            if (new_value not in new_vertex):
              new_vertex.extend([new_value])
    return new_vertex

  def lr1_goto_labels(self, vertex):
    answer = []
    for rule in self.lr1_graph[vertex]:
      to_pos = rule[1]
      dot_pos = to_pos.index(".")
      if (dot_pos != len(to_pos) - 1):
        answer.append(to_pos[dot_pos + 1])
    return answer
  
  def lr1_goto(self, from_vertex, label):
    new_vertex = []
    for rule in self.lr1_graph[from_vertex]:
      if (label not in rule[1]):
        continue
      dot_index = rule[1].index(".")
      if (dot_index != len(rule[1]) - 1 and rule[1][dot_index + 1] == label):
        new_rule = (rule[0], 
                    rule[1][:dot_index] + rule[1][dot_index + 1] + "." + rule[1][dot_index + 2:],
                    rule[2])
        if (new_rule not in new_vertex):
          new_vertex.append(new_rule)
    return new_vertex

  def lr1_build_table(self):
    self.letters = {"0": 0}
    pnt = 1
    for non_terminal in self.non_terminals:
      if (non_terminal != '0'):
        self.letters[non_terminal] = pnt
        pnt += 1
      
    for terminal in self.terminals:
      self.letters[terminal] = pnt
      pnt += 1

    self.letters["$"] = pnt


    self.table = [[None for _ in range(len(self.letters))] for _ in range(len(self.lr1_graph))]
    # 0 - just a number
    # 1 - shift
    # 2 - reduce

    for start, edges in self.edges.items():
      for to in edges:
        if (self.table[start][self.letters[to[1]]] != None):
          self.isLR1 = False
          assert False and 'Grammar is not LR1!'
        if (to[1] in self.non_terminals):
          self.table[start][self.letters[to[1]]] = (0, to[0])
        else:
          self.table[start][self.letters[to[1]]] = (1, to[0])

    for start, vertex in enumerate(self.lr1_graph):
      for rule in vertex:
        if (rule[1][-1] == '.'):
          ind = self.rules.index((rule[0], rule[1][:-1]))
          # if (self.table[start][self.letters[rule[2]]] != None):
            # continue
          self.table[start][self.letters[rule[2]]] = (2, ind)
    return True

  def lr1_reduce(self, word, stack):
    rule_number = self.table[stack[-1]][self.letters[word[0]]][1]
    template = self.rules[rule_number][1][::-1]
    current_word = ""
    while (len(stack) > 0 and current_word != template):
      stack.pop()
      current_word += stack[-1]
      stack.pop()
    
    if (current_word != template):
      return -1, -1, False

    stack.append(self.rules[rule_number][0])
    stack.append(self.table[stack[-2]][self.letters[stack[-1]]][1])

    return word, stack, True
  
  def lr1_shift(self, word, stack):
    token = word[0]
    vertex = stack[-1]
    table_rule = self.table[vertex][self.letters[token]]

    stack.append(token)
    stack.append(table_rule[1])
    return word[1:], stack

  def lr1_read_word(self, word):
    # word, stack, vertex, token
    word += "$"
    stack = [0]

    while (word != ""):
      token = word[0]
      vertex = stack[-1]
      if (self.table[vertex][self.letters[token]] == None):
        return False
      if (self.table[vertex][self.letters[token]][0] == 2):
        if (word == "$" and self.table[vertex][self.letters[token]][1] == 0):
          return True
        
        word, stack, possible = self.lr1_reduce(word, stack)
        if (not possible):
          return False
      else:
        word, stack = self.lr1_shift(word, stack)

    return True

  def lr1_check(self, word):
    self.remove_conflicts()
    self.clear_useless_letters()
    if (word == ""):
      return self.has_eps()
    for letter in word:
      if (letter not in self.terminals):
        return False
    # 0 is analogy of S' in handwritten rules
    self.rules.insert(0, ("0", "S"))
    self.non_terminals.append("0")
    self.lr1_first_precalc()

    self.calc_rules_from_terminal()

    self.lr1_graph = [[]]
    self.edges = {0: []}

    self.lr1_graph[0].append(("0", ".S", "$"))
    
    queue = [0]

    while (len(queue) > 0):
      current_vertex = queue[0]
      queue.pop(0)
      self.lr1_graph[current_vertex] = self.lr1_closure(self.lr1_graph[current_vertex])
      labels = list(set((self.lr1_goto_labels(current_vertex))))
      labels.sort() # for debug
      for label in labels:
        new_vertex = self.lr1_goto(current_vertex, label)
        new_vertex = self.lr1_closure(new_vertex)
        new_vertex.sort()
        found = False
        for i, el in enumerate(self.lr1_graph):
          if (el == new_vertex):
            found = True
            self.edges[current_vertex].append((i, label))
        if (not found):
          self.lr1_graph.append(new_vertex)
          self.edges[current_vertex].append((len(self.lr1_graph) - 1, label))
          self.edges[len(self.lr1_graph) - 1] = []
          queue.append(len(self.lr1_graph) - 1)

    if (not self.lr1_build_table()):
      return False

    answer = self.lr1_read_word(word)

    self.rules.remove(("0", "S"))
    self.non_terminals.remove("0")
    return answer

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

  @staticmethod
  def default_grammar5():
    start_terminal = "S"
    non_terminals = ["S", "F"]
    terminals = ["a", "b"]
    rules = [("S", "a"), ("S", "aFbF"), ("F", "aFb"), ("F", "")]
    return Grammar(non_terminals, terminals, rules, start_terminal)

  @staticmethod
  def default_grammar6():
    start_terminal = "S"
    non_terminals = ["S", "T"]
    terminals = ["a", "b", "c"]
    rules = [("S", "a"), ("S", "b"), ("S", "c"), ("T", "S")]
    return Grammar(non_terminals, terminals, rules, start_terminal)

  @staticmethod
  def default_grammar7():
    start_terminal = "S"
    non_terminals = ["S"]
    terminals = ["a", "b"]
    rules = [("S", "SaSb"), ("S", "")]
    return Grammar(non_terminals, terminals, rules, start_terminal)
  
def get_copy_of_grammar(grammar: Grammar):
  copy = grammar
  copy.found_words = set()
  copy.used = set()
  return copy
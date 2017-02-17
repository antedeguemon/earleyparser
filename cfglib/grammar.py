# -*- encoding: utf-8 -*-
import re
from cfglib.exceptions import *

class Grammar(object):
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def add(self, left, right):
        if left not in self.nonterminals:
            self.nonterminals.append(left)

        if left not in self.productions:
            self.productions[left] = [right]
        else:
            self.productions[left].append(right)

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_nonterminal(self, nonterminal):
        self.nonterminals.append(nonterminal)

    def is_terminal(self, symbol):
        for terminal in self.terminals:
            if terminal == symbol:
                return True
        return False

    def is_nonterminal(self, symbol):
        for nonterminal in self.nonterminals:
            if nonterminal == symbol:
                return True
        return False

# -*- encoding: utf-8 -*-

class Grammar(object):
    def __init__(self, start=None, productions={}):
        self.productions = productions
        self.start = start

    def add(self, left, right):
        if left not in self.productions:
            self.productions[left] = [right]
        else:
            self.productions[left].append(right)

    def set_start(self, nonterminal):
        self.start = nonterminal

    def is_terminal(self, symbol):
        return not self.is_nonterminal(symbol)

    def is_nonterminal(self, symbol):
        return symbol in self.productions

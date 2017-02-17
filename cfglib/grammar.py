# -*- encoding: utf-8 -*-
import re
from cfglib.exceptions import GrammarException, EmptyGrammarError, InvalidNonterminalError

class Grammar(object):
    '''
    Attributes:
        nonterminals    : list
        terminals       : list
        productions     : dict
        start           : str
    '''
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def test(self):
        if len(self.productions) == 0: # self.len
            raise EmptyGrammarError()
        if ('V' in self.nonterminals or 'V' in self.productions or
                'V' in self.terminals):
            raise InvalidNonterminalError()

    @staticmethod
    def len(productions):
        # Retorna a quantidade de regras de produções de uma gramática
        length = 0
        #[len(productions[]) for production in productions]
        for production in productions:
            length += len(productions[production])
        return length

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

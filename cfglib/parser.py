# -*- encoding: utf-8 -*-

class Row(object):
    def __init__(self, dot, left, right, pos, completeds=[]):
        self.dot = dot
        self.left = left
        self.right = right
        self.pos = pos
        self.start = pos[0]
        self.end = pos[1]
        self.completeds = completeds
    
    def show(self):
        dotted = ''.join(self.right)
        formated = (self.left + ' -> ' + ' ' + dotted[:self.dot] +
                    '\033[94m.\033[0m' + dotted[self.dot:])
        if len(formated) < 10:
            formated += '\t'
        formated += '\t\033[93m/'+str(self.start)+'\033[0m'
        print formated

    def get_next(self):
        return self.right[self.dot] if self.dot < len(self.right) else None

    def is_complete(self):
        return self.dot == len(self.right)
    
    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right and
                self.dot == other.dot and self.pos == other.pos)

class Table(object):
    def __init__(self, k):
        self.rows = []
        self.k = k

    def add_row(self, row, completeds=None):
        if row not in self.rows:
            self.rows.append(row)
            
        if completeds is not None and completeds not in row.completeds:
            row.completeds.append(completeds)

    def get_rows(self):
        return self.rows

    def __len__(self):
        return len(self.rows)

class Parser(object):
    def __init__(self, grammar):
        grammar.productions['GAMMA'] = [[grammar.start]]
        self.grammar = grammar
        self.tables = []
        self.words = []

    def add_table(self, k):
        self.tables.append(Table(k))

    def run(self, words):
        self.words = [[word] for word in words]
        self.init()

        for i in range(0, len(self.words) + 1):
            for row in self.tables[i].get_rows():
                if not row.is_complete():
                    if self.grammar.is_nonterminal(row.get_next()):
                        self.predict(row)
                    else:
                        self.scan(row)
                else:
                    self.complete(row)

    def init(self):
        # creates a GAMMA starting production and n+1 tables
        self.tables = []
        for i in range(0, len(self.words)+1):
            self.add_table(i)
        self.tables[0].add_row(Row(0, '', ['GAMMA'], (0, 0)))

    def scan(self, row):
        # creates a new row and copies the production that triggered this op
        # from the table[k-1] to the current table, advacing the pointer
        next_symbol = row.get_next()
        if row.end < len(self.words):
            atual = self.words[row.end][0]
            if next_symbol == atual:
                nrow = Row(1, next_symbol, [atual], (row.end, (row.end+1)))
                self.tables[row.end+1].add_row(nrow)

    def predict(self, row):
        # copies the productions from the nonterminal that triggered this op
        # with the new pointer in the begining of the right side
        b = row.get_next()
        if b in self.grammar.productions:
            for rule in self.grammar.productions[b]:
                self.tables[row.end].add_row(Row(0, b, rule, (row.end, row.end)))

    def complete(self, row):
        # advances all rows that were waiting for the current word
        for old_row in self.tables[row.start].get_rows():
            if (not old_row.is_complete() and 
                old_row.right[old_row.dot] == row.left):
                nrow = Row((old_row.dot+1), old_row.left, old_row.right, 
                           (old_row.start, row.end), old_row.completeds[:])
                self.tables[row.end].add_row(nrow, row)

    def show_tables(self):
        for table in self.tables:
            for row in table.rows:
                row.show()

    def make_node(self, row, relatives=[]):
        nodo = {'a': row.left}
        nodo['children'] = [self.make_node(_, []) for _ in row.completeds]        
        if not row.completeds:
            relatives += [row]
        if row.left == 'GAMMA':
            nodo['children'] += [{'a': self.words[_.start]} for _ in relatives 
                                  if _.start < len(self.words)]
        return nodo

    def get_completeds(self):
        # returns all rows that are in the GAMMA nonterminal
        completeds = []
        for row in self.tables[-1].get_rows():
            if row.left == 'GAMMA':
                completeds.append(row)
            
        # deletes GAMMA
        del self.grammar.productions['GAMMA']
        #for nonterminal in self.grammar.nonterminals:
        #    if nonterminal == '' or nonterminal == 'GAMMA':
        #        del nonterminal
        
        return completeds
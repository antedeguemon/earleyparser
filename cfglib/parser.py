# -*- encoding: utf-8 -*-

class Row(object):
    '''
    An Earley item.

    Attributes:
        dot         : int
        left        : str
        right       : list
        pos         : 2-uple
        start       : int
        end         : int
        completeds  : list
    '''
    def __init__(self, dot, left, right, pos, completeds=[]):
        self.dot = dot
        self.left = left
        self.right = right
        self.pos = pos
        self.start = pos[0]     # par (start, end)
        self.end = pos[1]
        self.completeds = completeds
    
    def show(self, raw=False):
        dotted = ''.join(self.right)
        formated = (self.left + ' -> ' + ' ' + dotted[:self.dot] +
                    '\033[94m.\033[0m' + dotted[self.dot:])
        if len(formated) < 10:
            formated += '\t'
        formated += '\t\033[93m/'+str(self.start)+'\033[0m'
        if raw:
            return formated
        print formated

    def get_next(self):
        # Retorna o símbolo após o ponteiro
        if self.dot < len(self.right):
            return self.right[self.dot]
        return None

    def is_complete(self):
        # Verifica se o item está completo seguindo o algoritmo de Earley
        return self.dot == len(self.right)
    
    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right and
                self.dot == other.dot and self.pos == other.pos)

class Table(object):
    '''
    Set of Earley items.

    Attributes:
        k       : int
        rows    : list
    '''
    def __init__(self, k):
        self.rows = []
        self.k = k  # id

    def add_row(self, row, completeds=None):
        # Insere um novo item de Earley na tabela
        if row not in self.rows:
            self.rows.append(row)
            
        if completeds is not None and completeds not in row.completeds:
            row.completeds.append(completeds)

    def get_rows(self):
        # Retorna o k da tabela
        return self.rows

    def __len__(self):
        return len(self.rows)

class Parser(object):
    '''
    Attributes:
        grammar : Grammar
        tables  : list
        words   : list
    '''
    def __init__(self, grammar):
        # adiciona a produção gamma
        grammar.productions['GAMMA'] = [[grammar.start]]
        grammar.nonterminals.append('GAMMA')
        grammar.nonterminals.append('')

        self.grammar = grammar
        self.tables = []
        self.words = []

    def add_table(self, k):
        '''Insere uma nova tabela'''
        self.tables.append(Table(k))

    def run(self, words):
        n_words = []
        for word in words:
            # necessário para que id seja único
            # porque em python, por algum motivo,
            # w = ['a', 'a'], id(w[0]) == id(w[1]) wtffff
            n_words.append([word])
        self.words = n_words
        self.init()

        for i in range(0, len(self.words) + 1):
            # old_len = len(self.tables[i])
            for row in self.tables[i].get_rows():
                if not row.is_complete():
                    # individualmente, ao contrario de table
                    if self.grammar.is_nonterminal(row.get_next()):
                        self.predict(row)
                    else:
                        self.scan(row)
                else:
                    self.complete(row)

    def init(self):
        # Cria uma produção GAMMA, necessária para montar a árvore de derivação.
        # Também cria n+1 tabelas, que serão preenchidas com itens de Earley, 
        # durante as etapas de parsing.
        self.tables = []
        for i in range(0, len(self.words)+1):
            self.add_table(i)
        self.tables[0].add_row(Row(0, '', ['GAMMA'], (0, 0)))

    def show_rows(self, table):
        '''Debugging da tabela'''
        for row in table.rows:
            row.show()

    def scan(self, row):
        # Cria uma nova Row, copiando a produção que resultou em seu trigger, da
        # tabela [k-1] para a tabela atual, avançando o ponto.
        next_symbol = row.get_next()
        if row.end < len(self.words):
            atual = self.words[row.end][0]
            if next_symbol == atual:
                self.tables[row.end+1].add_row(Row(1, next_symbol, [atual], 
                                                   (row.end, (row.end+1))))

    def predict(self, row):
        # Copia produções originais da variável que resultou em seu trigger, com
        # o novo ponto no início no lado direito. O novo start é o id da tabela
        # odne a produção foi chamada.
        b = row.get_next()
        if b in self.grammar.productions:
            for rule in self.grammar.productions[b]:
                self.tables[row.end].add_row(Row(0, b, rule, (row.end, row.end)))

    def complete(self, row):
        # Encontra e avança todas as rows que estavam esperando pela palavra
        # atual. 
        for old_row in self.tables[row.start].get_rows():
            if (not old_row.is_complete() and 
                old_row.right[old_row.dot] == row.left):
                self.tables[row.end].add_row(Row((old_row.dot+1), old_row.left, 
                                                 old_row.right, 
                                                 (old_row.start, row.end), 
                                                 old_row.completeds[:]), row)

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
        # Retorna todas as Rows na tabela final que chegaram ao estado GAMMA, ou
        # seja, que começaram no topo da derivação.
        completeds = []
        for row in self.tables[-1].get_rows():
            if row.left == 'GAMMA':
                completeds.append(row)
            
        # deleta a produção gamma
        del self.grammar.productions['GAMMA']
        for nonterminal in self.grammar.nonterminals:
            if nonterminal == '' or nonterminal == 'GAMMA':
                del nonterminal
        return completeds
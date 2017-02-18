# a simple context free grammar library
cfglib is a python library that offers functions to handle [CFGs](https://en.wikipedia.org/wiki/Context-free_grammar).
It was written originaly as a project for the formal languages and automatas class at UFRGS.

## Examples
### Creating a grammar that accepts binary numbers
```python
import cfglib
gr = cfglib.Grammar('S')
gr.add('S', ['0', 'S'])     # S = 0 S
gr.add('S', ['1', 'S'])     # S = 1 S
gr.add('S', ['1'])          # S = 1
gr.add('S', ['0'])          
```

### Checking if a word is accepted by a grammar using Earley parsing
Using the gr grammar created previously.
```python
pr = cfglib.Parser(gr)
pr.run('101011')

# all derivations that went into the first production
completeds = pr.get_completeds()
if len(completeds) == 0:
    # no derivation went into the first production
    print 'not accepted'
else:
    print 'accepted!'
```

### Building an AST from an Earley parsing
Using the parsing previosly made.
```python
# completeds should have 1 item as the word '101011' was recognized
def walk(node, level=0):
    print level*'-' + node['a']
    for child in node['children']:
        walk(child, level+1)

ast = pr.make_node(completeds[0])
walk(ast)
```

## Thanks to
- Algorithm described in the book "Linguagens Formais e Automatos" by Paulo Blauth.
- Algorithm described in "Speech and Language Processing: An introduction to natural language processing, computational linguistics, and speech recognition" by  D. Jurafsky and James H. Martin.
- Earley parsing AST building explanation by [loup-vaillant](loup-vaillant.fr/tutorials/earley-parsing/)
- [Earley-Parser by cskau](https://github.com/cskau/Earley-Parser)
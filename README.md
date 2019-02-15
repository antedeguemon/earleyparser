A simple earley parser.
```
pip install earleyparser 
```

## Examples
### Creating a grammar that accepts binary numbers
```python
gr = earleyparser.Grammar('S')
gr.add('S', ['0', 'S'])
gr.add('S', ['1', 'S'])
gr.add('S', ['1'])
gr.add('S', ['0'])          
```

### Checking if a word is accepted by a grammar using Earley parsing
Using the `gr` grammar previously created.
```python
pr = earleyparser.Parser(gr)
pr.run('101011')

# all derivations that went into the first production
completes = pr.get_completes()
if len(completes) == 0:
    # no derivation went into the first production
    print 'not accepted'
else:
    print 'accepted!'
```

### Building an AST from an Earley parsing
Using the parsing previously made.
```python
# completes should have 1 item as the word '101011' was recognized
def walk(node, level=0):
    print level*'-' + node['a']
    for child in node['children']:
        walk(child, level+1)

ast = pr.make_node(completes[0])
walk(ast)
```

## Bibliography
- _Linguagens Formais e Automatos_ by Paulo Blauth.
- _Speech and Language Processing: An introduction to natural language processing, computational linguistics, and speech recognition_ by D. Jurafsky and James H. Martin.
- [Earley parsing AST building explanation by loup-vaillant](loup-vaillant.fr/tutorials/earley-parsing/)
- [Earley-Parser by cskau](https://github.com/cskau/Earley-Parser)

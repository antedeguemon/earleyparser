# earleyparser

This is a Python implementation of the [Earley parser algorithm](https://en.wikipedia.org/wiki/Earley_parser).

It determines if a given word belongs to a specified context-free language. If the word
belongs to the specified language, it also mounts the parsing [derivation tree](https://en.wikipedia.org/wiki/Parse_tree).

## Installation

```
pip install earleyparser
```

## Examples

### Creating a grammar that accepts only binary numbers

```python
gr = earleyparser.Grammar('S')
gr.add('S', ['0', 'S'])
gr.add('S', ['1', 'S'])
gr.add('S', ['1'])
gr.add('S', ['0'])
```

### Checking if a word is accepted by a grammar

```python
pr = earleyparser.Parser(gr)
pr.run('101011')

# All derivations that went into the first production
completes = pr.get_completes()
if len(completes) == 0:
    print 'not accepted'
else:
    print 'accepted!'
```

### Building an AST from a parsing

```python
# The word `101011` was recognized by the grammer
# therefore, `completes` should have exactly one item.
def walk(node, level=0):
    print level*'-' + node['a']
    for child in node['children']:
        walk(child, level+1)

ast = pr.make_node(completes[0])
walk(ast)
```

## References

- [Linguagens Formais e Automatos book by Blauth Menezes](https://www.amazon.com/Linguagens-Formais-Aut%C3%B4matos-Did%C3%A1ticos-Portuguese-ebook/dp/B01863RJF6)
- [Earley parsing AST building explanation by loup-vaillant](loup-vaillant.fr/tutorials/earley-parsing/)
- [Earley-Parser by cskau](https://github.com/cskau/Earley-Parser)

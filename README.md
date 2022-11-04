# earleyparser

This is a Python implementation of the [Earley parser algorithm](https://en.wikipedia.org/wiki/Earley_parser).

It determines if a given word belongs to a specified context-free language. If the word
belongs to the specified language, it also mounts the parsing [derivation tree](https://en.wikipedia.org/wiki/Parse_tree).

**I made this library as a college homework. It is pretty crude and should be considered an experiment.**

### Limitations

Strings are not supported in grammars - instead of using strings, you should use
lists of characters:

```python
import earleyparser

grammar = earleyparser.Grammar('S')

# Sentence is composed of `<adjective> <noun>`
grammar.add('S', ['A', ' ', 'N'])

# Adjective is `happy`, `yellow` or `red`
grammar.add('A', ['h', 'a', 'p', 'p', 'y'])
grammar.add('A', ['y', 'e', 'l', 'l', 'o', 'w'])
grammar.add('A', ['r', 'e', 'd'])

# Noun is `dog` or `cat`
grammar.add('N', ['d', 'o', 'g'])
grammar.add('N', ['c', 'a', 't'])

parser = earleyparser.Parser(grammar)
parser.print_derivation_tree("red cat")

# Due to some bug, the parser doesn't reset its state after it is run, so we
# need to build it again.
parser = earleyparser.Parser(grammar)
parser.print_derivation_tree("yellow cat")

```

## Installation

```
pip install earleyparser
```

## Examples

### Creating a grammar that accepts only binary numbers

```python
import earleyparser

#
# Builds the following grammar:
# S -> 0S | 1S | 0 | 1
#
grammar = earleyparser.Grammar('S')
grammar.add('S', ['0', 'S'])
grammar.add('S', ['1', 'S'])
grammar.add('S', ['0'])
grammar.add('S', ['1'])

parser = earleyparser.Parser(grammar)
parser.run('101011')

#
# Checks if a word is accepted by a grammar
#
derivations = parser.get_completes()
if len(derivations) == 0:
    print('Not accepted')
else:
    print('Accepted!')

#
# Prints a derivation tree
#
parser = earleyparser.Parser(grammar)
parser.print_derivation_tree("0101011")
```

The resulting derivation from the above snippet is:

```
GAMMA
..S
....0
....S
......1
......S
........0
........S
..........1
..........S
............0
............S
..............1
..............S
................1
```


## References

- [Linguagens Formais e Automatos book by Blauth Menezes](https://www.amazon.com/Linguagens-Formais-Aut%C3%B4matos-Did%C3%A1ticos-Portuguese-ebook/dp/B01863RJF6)
- [Earley parsing AST building explanation by loup-vaillant](loup-vaillant.fr/tutorials/earley-parsing/)
- [Earley-Parser by cskau](https://github.com/cskau/Earley-Parser)

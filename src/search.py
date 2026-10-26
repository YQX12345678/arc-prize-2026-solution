"""Program search with pruning over the DSL."""
from itertools import product
from .dsl import OPS, shape


def _apply(grid, program):
    g = grid
    for name in program:
        fn = OPS.get(name)
        if fn is None:
            return None
        g = fn(g)
        if g is None:
            return None
    return g


def _consistent(program, train_pairs):
    for inp, out in train_pairs:
        pred = _apply(inp, program)
        if pred != out:
            return False
    return True


def search(train_pairs, max_depth=3):
    """Return the shortest program consistent with all training pairs."""
    names = list(OPS.keys())
    for depth in range(1, max_depth + 1):
        for program in product(names, repeat=depth):
            if _consistent(program, train_pairs):
                return list(program)
    return None

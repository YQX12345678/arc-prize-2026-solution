"""Consistency evaluation for ARC candidates."""
from .dsl import shape


def example_consistency(candidate, train_pairs):
    if candidate is None:
        return 0.0
    ok = 0
    for inp, out in train_pairs:
        if candidate(inp) == out:
            ok += 1
    return ok / max(1, len(train_pairs))


def grid_similarity(a, b):
    if shape(a) != shape(b):
        return 0.0
    total = sum(len(r) for r in a)
    if total == 0:
        return 1.0
    same = sum(1 for ra, rb in zip(a, b) for x, y in zip(ra, rb) if x == y)
    return same / total

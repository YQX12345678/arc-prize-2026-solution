"""Lightweight test-time training stub.

A tiny per-task classifier over cell colors; trained on the few
input/output pairs of the current ARC task before predicting.
"""
import numpy as np


class TinyCellClassifier:
    def __init__(self, n_colors=10):
        self.n_colors = n_colors
        self.table = np.zeros((n_colors, n_colors))

    def fit(self, pairs):
        for inp, out in pairs:
            h = min(len(inp), len(out))
            w = min(len(inp[0]), len(out[0]))
            for y in range(h):
                for x in range(w):
                    self.table[inp[y][x], out[y][x]] += 1

    def predict(self, grid):
        out = []
        for row in grid:
            new_row = []
            for v in row:
                new_row.append(int(np.argmax(self.table[v])) if self.table[v].sum() > 0 else v)
            out.append(new_row)
        return out

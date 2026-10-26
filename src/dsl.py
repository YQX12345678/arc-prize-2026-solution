"""Tiny DSL for ARC grid transformations.

Each op maps a grid (list of list of int) to a grid, or None if inapplicable.
"""
import copy


def shape(g):
    return (len(g), len(g[0]) if g and g[0] else 0)


def rotate90(g):
    return [list(r) for r in zip(*g[::-1])]


def rotate180(g):
    return [row[::-1] for row in g[::-1]]


def rotate270(g):
    return [list(r) for r in zip(*g)][::-1]


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return [row[:] for row in g[::-1]]


def transpose(g):
    return [list(r) for r in zip(*g)]


def crop_bbox(g):
    cells = [(y, x) for y, row in enumerate(g) for x, v in enumerate(row) if v != 0]
    if not cells:
        return None
    ys = [c[0] for c in cells]
    xs = [c[1] for c in cells]
    y0, y1, x0, x1 = min(ys), max(ys), min(xs), max(xs)
    return [row[x0:x1 + 1] for row in g[y0:y1 + 1]]


def pad_to(g, h, w, fill=0):
    out = [[fill] * w for _ in range(h)]
    for y in range(min(h, len(g))):
        for x in range(min(w, len(g[y]))):
            out[y][x] = g[y][x]
    return out


def most_common_color(g):
    from collections import Counter
    c = Counter(v for row in g for v in row if v != 0)
    return c.most_common(1)[0][0] if c else 0


def recolor(g, src, dst):
    out = [row[:] for row in g]
    hit = False
    for y in range(len(out)):
        for x in range(len(out[y])):
            if out[y][x] == src:
                out[y][x] = dst
                hit = True
    return out if hit else None


OPS = {
    "rot90": rotate90,
    "rot180": rotate180,
    "rot270": rotate270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "crop_bbox": crop_bbox,
}

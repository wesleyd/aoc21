#!/usr/bin/env python3

from collections import defaultdict
import difflib

test_input = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

def parse(input):
    graph = defaultdict(list)
    for line in input.splitlines():
        l, r = line.split('-')
        graph[l].append(r)
        graph[r].append(l)
    return graph

def candidates(graph, here, path):
    for nxt in graph[here]:
        if nxt not in path or nxt.isupper():
            yield nxt

def walk(graph, path=None, z='end'):
    if path is None:
        path = ['start']
    for nxt in candidates(graph, path[-1], path):
        path2 = path + [nxt]
        if nxt == z:
            yield path2
        yield from walk(graph, path2, z)

def alphabetically(paths):
    return '\n'.join(sorted([','.join(path) for path in paths])) + '\n'

def count(paths):
    return sum(1 for x in paths)

want = """\
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end
"""
got = alphabetically(walk(parse(test_input)))
assert got == want, "first graph:\ngot:\n%s\nwant:\n%s\n" % (got, want)

slightly_larger_example = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""
got = alphabetically(walk(parse(slightly_larger_example)))
want = """\
start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end
"""
assert got == want, "larger example: (-want + got):\n%s" % '\n'.join(difflib.unified_diff(want.splitlines(), got.splitlines()))

even_larger_example = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""
got = count(walk(parse(even_larger_example)))
want = 226
assert got == want, "even_larger_example: got %d, want %d" % (got, want)

with open('inputs/day12.input') as f:
    g = parse(f.read())
    n = count(walk(g))
    print('Day 12 part 1 => %d' % n)

### Part 2

def no_little_dups(path):
    smalls = list(filter(lambda x: x.islower(), path))
    return len(smalls) == len(set(smalls))

def candidates(graph, here, path):
    for nxt in graph[here]:
        if nxt.isupper():
            yield nxt
        elif nxt not in path:
            yield nxt
        elif no_little_dups(path) and nxt not in ('start', 'end'):
            yield nxt

want = """\
start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end
"""
got = alphabetically(walk(parse(test_input)))
assert got == want, "simple input (36), one little dup allowed: (-want +got):\n%s" % ('\n'.join(difflib.unified_diff(want.splitlines(), got.splitlines())))

got = count(walk(parse(slightly_larger_example)))
want = 103
assert got == want, "slightly larger example, one wee dup ok: got %d, want %d" % (got, want)

got = count(walk(parse(even_larger_example)))
want = 3509
assert got == want, "even larger example, one wee dup ok: got %d, want %d" % (got, want)

with open('inputs/day12.input') as f:
    g = parse(f.read())
    n = count(walk(g))
    print('Day 12 part 2 => %d' % n)  # => 149385  (Slow: tens of seconds!!

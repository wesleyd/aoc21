#!/usr/bin/env python3

test_input = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

matches = {
    '{': '}',
    '}': '{',
    '[': ']',
    ']': '[',
    '<': '>',
    '>': '<',
    '(': ')',
    ')': '(',
}

def bad(line):
    stack = []
    for c in line:
        if c in ('(', '{', '[', '<'):
            stack.append(c)
        elif c in matches:
            b = stack.pop()
            if matches[c] != b:
                return c
    return False

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def score(input):
    n = 0
    for line in input.splitlines():
        c = bad(line)
        if c:
            n+= scores[c]
    return n

got = score(test_input)
want = 26397
if got != want:
    raise Exception('score(test_input): got %d, want %d' % (got, want))

with open('inputs/day10.input') as f:
    sc = score(f.read())
    print('Day 10 Part 1 => %d' % sc)  # => 240123

### Part 2

cscores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def goodness(line):
    stack = []
    for c in line:
        if c in ('(', '{', '[', '<'):
            stack.append(c)
        elif c in matches:
            b = stack.pop()
            if matches[c] != b:
                return False
    stack.reverse()
    closers = [matches[c] for c in stack]
    n = 0
    for x in closers:
        n = n*5 + cscores[x]
    return n

wants = {
    '[({(<(())[]>[[{[]{<()<>>': 288957,
    '[(()[<>])]({[<{<<[]>>(': 5566,
    '(((({<>}<{<{<>}{[]{[]{}': 1480781,
    '{<[[]]>}<{[{[{[]{()[[[]': 995444,
    '<{([{{}}[<[[[<>{}]]]>[]]': 294,
}
for input, want in wants.items():
    got = goodness(input)
    if got != want:
        raise Exception('goodness(%s): got %d, want %d' % (input, got, want))

def best(input):
    sc = list(filter(bool, map(goodness, input.splitlines())))
    sc.sort()
    return sc[len(sc)//2]

got = best(test_input)
want = 288957
if got != want:
    raise Exception('best(test_input): got %d, want %d' % (got, want))

with open('inputs/day10.input') as f:
    sc = best(f.read())
    print('Day 10 Part 2 => %d' % sc)  # =>  3260812321

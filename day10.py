#!/usr/bin/env python

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
    '}': '{',
    ']': '[',
    '>': '<',
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

with open('day10.input') as f:
    sc = score(f.read())
    print('Day 10 Part 1 => %d' % sc)  # => 240123

### Part 2

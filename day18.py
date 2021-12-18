#!/usr/bin/env python3

import math

def parser(s):
    n = None
    for c in s:
        if c.isdigit():
            if n is None:
                n = int(c)
            else:
                n = n*10 + int(c)
        else:
            if n is not None:
                yield n
                n = None
            yield c

def parse(s):
    # print("parser'ing %s" % s)
    return list(parser(s))

def unparse(sf):
    return ''.join([str(c) for c in sf])

def explode(s):
    sf = parse(s)
    depth = 0
    i = 0
    while i < len(sf):
        #print('%s DEPTH(%s) %s' % (sf[:i], sf[i], sf[i+1:]))
        if sf[i] == ']':
            depth -= 1
        elif sf[i] == '[':
            depth += 1
            if depth > 4:
                #print ('At depth!')
                l = sf[i+1]
                assert sf[i+2] == ','
                r = sf[i+3]
                assert sf[i+4] == ']'
                #print('Exploding [%s,%s]' % (l, r))
                lhs = sf[:i]
                rhs = sf[i+5:]
                #print('  lhs is %s' % lhs)
                #print('  rhs is %s' % rhs)
                for j in range(len(lhs)-1, -1, -1):
                    if isinstance(lhs[j], int):
                        lhs[j] += l
                        break
                for j in range(len(rhs)):
                    if isinstance(rhs[j], int):
                        rhs[j] += r
                        break
                return unparse(lhs + [0] + rhs)
        i += 1
    return s

assert explode('[[[[[9,8],1],2],3],4]') == '[[[[0,9],2],3],4]'
assert explode('[7,[6,[5,[4,[3,2]]]]]') == '[7,[6,[5,[7,0]]]]'
assert explode('[[6,[5,[4,[3,2]]]],1]') == '[[6,[5,[7,0]]],3]'
assert explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
assert explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'

def snailsplit(s):
    sf = parse(s)
    for i in range(len(sf)):
        if isinstance(sf[i], int) and sf[i] >= 10:
            l = sf[i] // 2
            r = math.ceil(sf[i]/2)
            return unparse(sf[:i] + [ '[', l, ',', r, ']' ] + sf[i+1:])
    return s

assert snailsplit('[[[[0,7],4],[15,[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
assert snailsplit('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'

def reduce1(s):
    e = explode(s)
    if e != s:
        #print('after explode:  %s' % e)
        return e
    r = snailsplit(s)
    if r != s:
        #print('after split:   %s' % r)
        return r
    return s

def snailreduce(s):
    while True:
        r = reduce1(s)
        if r == s:
            return s
        s = r

def snailadd(a, b):
    c = '[' + a + ',' + b + ']'
    #print('after addition: %s' % c)
    return snailreduce(c)

assert snailadd('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

def snailaddlines(ss):
    lines = ss.splitlines()
    x, lines = lines[0], lines[1:]
    for line in lines:
        x = snailadd(x, line)
    return x

assert snailaddlines("""\
[1,1]
[2,2]
[3,3]
[4,4]
""") == '[[[[1,1],[2,2]],[3,3]],[4,4]]'
assert snailaddlines("""\
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
""") == '[[[[3,0],[5,3]],[4,4]],[5,5]]'
assert snailaddlines("""\
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
""") == '[[[[5,0],[7,4]],[5,5]],[6,6]]'
assert snailaddlines("""\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""") == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

def magnitude(s):
    def helper(lst):
        if isinstance(lst, int):
            return lst
        elif len(lst) == 2:
            return 3*helper(lst[0]) + 2*helper(lst[1])
    return helper(eval(s))

assert magnitude('[9,1]') == 29
assert magnitude('[1,9]') == 21
assert magnitude('[[9,1],[1,9]]') == 129
assert magnitude('[[1,2],[[3,4],5]]') == 143
assert magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384
assert magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445
assert magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791
assert magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]') == 1137
assert magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488
assert magnitude(snailaddlines("""\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""")) == 4140

with open('inputs/day18.input') as f:
    print("Day 18 part 1 => %s" % magnitude(snailaddlines(f.read())))

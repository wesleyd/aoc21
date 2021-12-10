#!/usr/bin/env python3

from itertools import permutations

day8_test_input = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

def parse(input):
    lines = input.splitlines()
    codes = []
    for line in lines:
        left, right = line.split(' | ')
        inputs = left.split()
        outputs = right.split()
        codes.append((left.split(), right.split()))
    return codes


# 0 => 'abcefg' => 6
# 1 => 'cf' => 2 (unique)
# 2 => 'acdeg' => 5
# 3 => 'acdfg' => 5
# 4 => 'bcdf' => 4 (unique)
# 5 => 'abdfg' => 5
# 6 => 'abdefg' => 6
# 7 => 'acf' => 3 (unique)
# 8 => 'abcdefg' => 7 (unique)
# 9 => 'abcdfg' => 6

def nuniques(codes):
    n = 0
    for code in codes:
        _, outputs = code
        for output in outputs:
            if len(output) in {2, 3, 4, 7}:
                n += 1
    return n

got = nuniques(parse(day8_test_input))
want = 26
if got != want:
    raise Exception('part1 test: got %d, want %d' % (got, want))

with open('day08.input') as f:
    day8_input = f.read()
    day8a = nuniques(parse(day8_input))
    print('Day 8 Part 1  =>', day8a)  # => 272

### Part 2

numbers2letters = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]
letters2numbers = {}
for i in range(len(numbers2letters)):
    letters2numbers[numbers2letters[i]] = i

alphabet = 'abcdefg'

def makeperm(s):
    perm = {}
    for i in range(len(alphabet)):
        perm[alphabet[i]] = s[i]
        #perm[s[i]] = alphabet[i]
    return perm

input = 'badfgac'
got = makeperm(input)
want = {
    'a': 'b',
    'b': 'a',
    'c': 'd',
    'd': 'f',
    'e': 'g',
    'f': 'a',
    'g': 'c',
}
if got != want:
    raise Exception('bad makeperm: got %s, want %s' % (got, want))

def permute(perm, s):
    out = ''.join([perm[c] for c in s])
    # print('permute(%s, %s) => %s' % (perm, s, out))
    return out

p = makeperm('badfgac')
permute(p,'abcdefg')

perm = makeperm('gbadfac')
got = permute(perm, 'abcdefg')
want = 'gbadfac'
if got != want:
    raise Exception('bad permute: got %s, want %s' % (got, want))

#def ssort(s):
#    sort(s.split())

# ''.join(sorted('bac'))

def perm2string(perm):
    return ''.join([perm[c] for c in 'abcdefg'])

def valid(perm, enums):
    """Whether perm transforms enums into valid segment display."""
    if len(enums) != 10:
        raise Exception('enums must be ten entries long, not %d: %s.' % (len(enums), enums))
    for eenum in enums:
        o = ''.join(sorted(permute(perm, enum)))
        if letters2numbers.get(o, -1) == -1:
            return False
    return True

def candidates(enums):
    """All permutations that *could* fit enums."""
    for p in permutations('abcdefg'):
        perm = makeperm(p)
        if valid(perm, enums):
            yield perm

# list(candidates("edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec".split()))

def apply(perm, rights):
    display = []
    for r in rights:
        o = ''.join(sorted(permute(perm, r)))
        n = letters2numbers.get(o, -1)
        if n == -1:
            # perm *can't* fit rights...
            print('  permute(%s, %s) => %s, not a number' % (perm2string(perm), r, o))
            return None
        display.append(str(n))
    print('  permute(%s, %s) => %s' % (perm2string(perm), r, ''.join(display)))
    return ''.join(display)

def invert(perm):
    iperm = {}
    for k, v in perm.items():
        iperm[v] = k
    return iperm

def solutions(line):
    lhs, rhs = line.split('|')
    lefts, rights = lhs.split(), rhs.split()
    for perm in candidates(lefts):
        print('Considering candidate %s...' % perm2string(perm))
        #perm = invert(perm)
        display = apply(perm, rights)
        if display is not None:
            yield (perm2string(perm), int(display))

#dict(solutions("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe"))
#dict(solutions("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"))
#dict(solutions("edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc"))

dict(solutions("gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"))

dict(solutions("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"))

def solve(line):
    lhs, rhs = line.split('|')
    lefts, rights = lhs.split(), rhs.split()
    for perm in candidates(lefts):
        #perm = invert(perm)
        display = apply(perm, rights)
        if display is not None:
            return perm2string(perm, int(display))
    return None

# solve('be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe')

tests = {
        #"acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf": 5353,
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe": 8394,
        #"edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc": 9781,
        #"fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg": 1197,
        #"fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb": 9361,
        #"aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea": 4873,
        #"fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb": 8418,
        #"dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe": 4548,
        #"bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef": 1625,
        #"egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb": 8717,
        #"gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce": 4315,
}
for inp, want in tests.items():
    got = solve(inp)
    if got != want:
        raise Exception('solve(%s): got %s, want %s' % (inp, got, want))



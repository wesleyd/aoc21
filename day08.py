#!/usr/bin/env python3

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
# 7 => 'acf' => 3 (unique0
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

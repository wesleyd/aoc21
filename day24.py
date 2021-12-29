#!/usr/bin/env python3

import math
import sys

#import os
#import subprocess

from collections import defaultdict
import functools

with open('inputs/day24.input') as f:
   day24_program = f.read()

def to_model(x, n=14):
    """Converts a regular int to a model string, with only 1-9"""
    m = []
    for i in range(n):
        z = x % 9
        x //= 9
        m.append(z+1)
    return ''.join(str(c) for c in m[::-1])
assert to_model(0) == '11111111111111'
assert to_model(1) == '11111111111112'
assert to_model(1,3) == '112'

#def from_model(m):
#    """Converts a model string back to an int again"""
#    n = 0
#    for c in m:
#        assert c in '123456789'
#        d = int(c) - 1
#        n = n * 9 + d
#    return n
#assert from_model('11111111111111') == 0
#assert from_model(to_model(1234567890)) == 1234567890

def string_to_model(s):
    m = 0
    allowed = range(9)
    for c in s:
        d = int(c) - 1
        if d not in allowed:
            raise Exception('bad digit %c in s (not in [1,9])' % c)
        m = m*9 + d
    return m
assert string_to_model('123') == (1-1)*81 + (2-1)*9 + (3-1) == 11
assert string_to_model('234') == (2-1)*81 + (3-1)*9 + (4-1)  == 102
assert string_to_model('9876') == (9-1)*729 + (8-1)*81 + (7-1)*9 + 6-1 == 6458
assert string_to_model('9999') > string_to_model('999')
assert string_to_model('999') > string_to_model('998')
assert string_to_model('999') > string_to_model('111')
assert string_to_model('112') < string_to_model('121')
#assert string_to_model('1121') > string_to_model('121')

def model_to_string(m, n):
    p = []
    for i in range(n):
        d = (m % 9) + 1
        m //= 9
        p.append(str(d))
    p.reverse()
    return ''.join(p)
assert model_to_string(11, 3) == '123'
assert model_to_string(102, 3) == '234'
assert model_to_string(6458, 4) == '9876'
assert model_to_string(6458, 6) == '119876'

def chunkify(program):
    """split programs into pieces that begin with 'inp '"""
    programs = []
    prev = []
    for line in program.splitlines():
        if line.startswith("inp"):
            if prev:
                programs.append('\n'.join(prev))
            prev = [line]
        else:
            prev.append(line)
    if prev:
        programs.append('\n'.join(prev))
    return programs
with open('inputs/day24.input') as f:
    day24_programs = chunkify(f.read())
    assert(len(day24_programs)) == 14

def parse(code, name):
    p = [
        "def %s(m, z=0):" % name,
        "  i, w, x, y = 0, 0, 0, 0"
    ]
    for linenum, line in enumerate(code.splitlines()):
        pieces = line.split()
        match pieces:
            case ('inp', r):
                p.append("  %s = int(m[i])" % r)
                p.append("  i += 1")
                #p.append("  print('Read %%d into %s' %% %s)" % (r, r))
                #p.append("  print('w=%s,x=%s,y=%s,z=%s' % (w,x,y,z))")
            case ('add', a, b):
                p.append("  %s += %s" % (a, b))
            case ('mul', a, b):
                p.append("  %s *= %s" % (a, b))
                #p.append("  print('after* w=%s,x=%s,y=%s,z=%s' % (w,x,y,z))")
            case ('div', a, b):
                p.append("  %s = int(%s / %s)" % (a, a, b))
            case ('mod', a, b):
                p.append("  %s %%= %s" % (a, b))
            case ('eql', a, b):
                #p.append("  print('before= w=%s,x=%s,y=%s,z=%s' % (w,x,y,z))")
                p.append("  %s = 1 if %s == %s else 0" % (a, a, b))
                #p.append("  print('after= w=%s,x=%s,y=%s,z=%s' % (w,x,y,z))")
            case _:
                raise Exception('unknown command %s at line %d' % (pieces, linenum))
    p.append("  return z")
    return '\n'.join(p)
exec(parse(day24_program, "day24_function"))

exec(parse("""\
inp z
mul z -1
""", "alu_negate"))
assert alu_negate('5') == -5
assert alu_negate('8') == -8

exec(parse("""\
inp z
inp x
mul z 3
eql z x
""", "alu_is3x"))
assert alu_is3x('13') == 1  
assert alu_is3x('23') != 1
assert alu_is3x('39') == 1
assert alu_is3x('49') != 1

def back_chunk(chunk, goals):
    zw = {}
    g = {}
    exec(parse(day24_programs[chunk], 'my_function'), g)
    f = g['my_function']
    biggest_goal = max(goals.keys())
    last_under = 0
    for i in range(9, 0, -1):
        w = str(i)
        z = 0
        while True:
            z2 = f(w, z)
            if z2 in goals:
                if z in zw:
                    if w > zw[z]:
                        #print('Found a *better* z2 in goals: z=%d w=%s (better than %s)' % (z, 2, zw[z]))
                        zw[z] = w + goals[z2]
                    else:
                        #print('Ignoring worser z2 in goals: z=%d w=%s (worse than %s)' % (z, 2, zw[z]))
                        1
                else:
                    #print('Found a z2 in goals: z=%d w=%s' % (z, 2))
                    zw[z] = w + goals[z2]
            if z2 <= biggest_goal:
                last_under = z
            if z - last_under > 26:
                # If the last 26 z's have been bigger than our biggest goal, we can stop looking!
                #print('Stopping looking for a (z,w=%s) -> %d goals <= %d' % (w, len(goals), biggest_goal))
                break
            z += 1
    return zw

goals_1 = back_chunk(-1, {0: ''})

goals_2 = back_chunk(-2, goals_1)

goals_3 = back_chunk(-3, goals_2)

goals_4 = back_chunk(-4, goals_3)

goals_5 = back_chunk(-5, goals_4)

goals_6 = back_chunk(-6, goals_5)

goals_7 = back_chunk(-7, goals_6)

goals_8 = back_chunk(-8, goals_7)

goals_9 = back_chunk(-9, goals_8)

goals_10 = back_chunk(-10, goals_9)

goals_11 = back_chunk(-11, goals_10)

goals_12 = back_chunk(-12, goals_11)

goals_13 = back_chunk(-13, goals_12)

goals_14 = back_chunk(-14, goals_13)  # => {0: '51939397989999'}






for 


# At top level because exec is crippled...
#lastn = 1
#zmax = 1000
#day24_lastn_code = '\n'.join(day24_programs[-lastn:])
#exec(parse(day24_lastn_code, "day24_lastn"))
#iterate_lastn(lastn, zmax=zmax)

#if len(sys.argv) > 1:
#    chunk = sys.argv[1]
#else:
#    chunk='-1'
#print("Choosing chunk(s) %s" % chunk)
#
#if ':' in chunk:
#    my_code = '\n'.join(eval('day24_programs[%s]' % chunk))
#else:
#    my_code = eval('day24_programs[%s]' % chunk)
#
#if len(sys.argv) > 2:
#    w = sys.argv[2]
#else:
#    w = '1'
#exec(parse(my_code, "my_function"))
#z = 0
#while True:
#    z2 = my_function(w, z)
#    print('chunk[%s](w=%s,z=%d) => %d' % (chunk, w, z, z2))
#    z += 1
#
#int('1' + '0'*11, 9)
#math.pow(2,32)


#for nchunk in range(14):
#    outputs = set()
#    for z in range(26):
#        exec(parse(day24_programs[nchunk], "local_function"))
#        z2 = local_function('1', z)
#        outputs.add(z2)
#    if len(outputs) == 2:
#        print('Chunk %d has two periods' % nchunk)
#    elif len(outputs) == 26:
#        print('Chunk %d is straight-up incrementing' % nchunk)
#    else:
#        print("Chunk %d is I don't know what" % nchunk)

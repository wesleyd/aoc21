#!/usr/bin/env python3

import operator

with open('inputs/day24.input') as f:
   day24_program = f.read()

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
            case ('add', a, b):
                p.append("  %s += %s" % (a, b))
            case ('mul', a, b):
                p.append("  %s *= %s" % (a, b))
            case ('div', a, b):
                p.append("  %s = int(%s / %s)" % (a, a, b))
            case ('mod', a, b):
                p.append("  %s %%= %s" % (a, b))
            case ('eql', a, b):
                p.append("  %s = 1 if %s == %s else 0" % (a, a, b))
            case _:
                raise Exception('unknown command %s at line %d' % (pieces, linenum))
    p.append("  return z")
    return '\n'.join(p)

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

def work_backwards():
    goals = {0: ''}  # 
    for i in range(-1, -15, -1):
        goals = back_chunk(i, goals)
    return list(goals.values())[0]

print("Day 24 part 1 =>", work_backwards())

def back_chunk(chunk, goals):
    zw = {}
    g = {}
    exec(parse(day24_programs[chunk], 'my_function'), g)
    f = g['my_function']
    biggest_goal = max(goals.keys())
    last_under = 0
    for i in range(1, 10, 1):
        w = str(i)
        z = 0
        while True:
            z2 = f(w, z)
            if z2 in goals:
                if z in zw:
                    if w < zw[z]:
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

print("Day 24 part 2 =>", work_backwards())

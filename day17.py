#!/usr/bin/env python3

import re
import math

test_input = 'target area: x=20..30, y=-10..-5'

def parse(input):
    left, right, bottom, top = [int(x) for x in re.findall(r'-?[0-9]+', input)]
    return (left, right, bottom, top)

assert parse(test_input) == (20, 30, -10, -5)

#    ok  |  ok  | stop
#    ok  | hit! | stop
#   stop | stop | stop

def shoot(trench, vx, vy):
    left, right, bottom, top = trench
    x,y = 0, 0
    trajectory = []
    while True:
        trajectory.append((x,y))
        if bottom <= y and y <= top and left <= x and x <= right:
            # Hit!
            return ("hit", trajectory)
        if y < bottom or x > right:
            # We overshot. Stop looking.
            return ("overshoot", trajectory)
        # Keep shooting...
        y += vy
        x += vx
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

#trench = parse(test_input)
#shoot(trench, 7, 2)
#shoot(trench, 6, 3)
#shoot(trench, 9, 0)

def maxy(trajectory):
    return max([p[1] for p in trajectory])

def holdvy(trench, vy):
    left, right, bottom, top = trench
    best_apogee, best_vx = None, None
    for vx in range(1, right):
        (outcome, trajectory) = shoot(trench, vx, vy)
        last = trajectory[len(trajectory)-1]
        apogee = maxy(trajectory)
        #print('Tried v=(%d,%d): got %s' % (vx,vy,outcome))
        if outcome == 'hit' and (best_apogee is None or best_apogee < apogee):
            best_apogee = apogee
            best_vx = vx
        # Keep increasing vx until we end up in the top right zone...
        if last[0] > right and last[1] > top:
            return best_vx
        vx += 1
    return best_vx

def raze(trench):
    left, right, bottom, top = trench
    vy = bottom
    best_apogee, best_v = None, None
    nmisses = 0
    while True:
        vx = holdvy(trench, vy)
        if not vx:
            #print("No vx for vy=%d" % vy)
            nmisses += 1
        else:
            (outcome, trajectory) = shoot(trench, vx, vy)
            assert outcome == 'hit'
            apogee = maxy(trajectory)
            if best_apogee is None or best_apogee < apogee:
                best_apogee = apogee
                best_v = (vx, vy)
        vy += 1
        #if nmisses > abs(bottom - top)+abs(left-right):  # ¯\_(ツ)_/¯
        if nmisses > 1000:  # ¯\_(ツ)_/¯
            return (best_apogee, best_v)

trench = parse(test_input)
raze(trench)

with open('inputs/day17.input') as f:
    apogee, v = raze(parse(f.read()))
    print("Day 17 Part 1 => %s (v=%s)" % (apogee, v))

# Part 2

# 1 <= vx <= right
# bottom <= vy
# Iterate vy until it "misses"

def vxmin(left):
    """The smallest vx that will just barely reach the trench."""
    return (1 + math.isqrt(1 + 8*left)) // 2

def holdvy2(trench, vy):
    left, right, bottom, top = trench
    for vx in range(vxmin(left), right+1):
        (outcome, trajectory) = shoot(trench, vx, vy)
        #print('Tried v=(%d,%d): got %s' % (vx,vy,outcome))
        if outcome == 'hit':
            yield vx
        vx += 1

def raze2(trench):
    left, right, bottom, top = trench
    vy = bottom
    nhits = 0
    while vy <= -bottom:
        for vx in holdvy2(trench, vy):
            yield (vx, vy)
        vy += 1

def count_hits(trench):
    return sum([1 for p in raze2(trench)])

trench = parse(test_input)
assert count_hits(trench) == 112

#test_results = """\
#23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
#25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
#8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
#26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
#20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
#25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
#25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
#8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
#24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
#7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
#23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
#27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
#8,-2    27,-8   30,-5   24,-7
#"""
#def extract_pairs(input):
#    for line in test_results.splitlines():
#        for pair in re.split('\s+', line):
#            yield tuple(map(int, pair.split(',')))
#
#my_hits = []
#for vx, vy in raze2(trench):
#    # print('%d hits v=(%d,%d)' % (nhits, vx, vy))
#    my_hits.append((vx,vy))
#
#want = sorted(list(extract_pairs(test_results)))
#got = sorted(my_hits)
#set(want).difference(set(got))
#set(got).difference(set(want))

with open('inputs/day17.input') as f:
    trench = parse(f.read())
    print('Day 17 Part 2 => %d' % count_hits(trench))

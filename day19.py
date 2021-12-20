#!/usr/bin/env python3

from itertools import permutations

with open('day19.test_input') as f:
    test_input = f.read()

def parse(input):
    """Returns a list of sensors. A sensor is a set of beacons. A beacon is a tuple (x,y,z)."""
    pieces = input.split('\n\n')
    scanners = []
    for piece in pieces:
        lines = piece.splitlines()[1:]
        beacons = set(tuple(map(int, line.split(','))) for line in lines)
        scanners.append(set(beacons))
    return scanners
test_sensors = parse(test_input)
assert len(test_sensors) == 5
assert len(test_sensors[0]) == 25

#def rotations(beacon):
#    rots = []
#    for p in permutations(range(3)):
#        b2 = [beacon[i] for i in p]
#        for orientation in [(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]:
#            rots.append(tuple([p * q for p, q in zip(b2, orientation)]))
#    return set(rots)
#assert rotations(((1, 2, 3))) == {
#        (1, 2, 3), (-1, 2, 3), (1, -2, 3), (1, 2, -3),
#        (1, 3, 2), (-1, 3, 2), (1, -3, 2), (1, 3, -2),
#        (2, 1, 3), (-2, 1, 3), (2, -1, 3), (2, 1, -3),
#        (2, 3, 1), (-2, 3, 1), (2, -3, 1), (2, 3, -1),
#        (3, 1, 2), (-3, 1, 2), (3, -1, 2), (3, 1, -2),
#        (3, 2, 1), (-3, 2, 1), (3, -2, 1), (3, 2, -1)
#}

def frotations():
    #for p in [(0,1,2), (1,2,0), (2,0,1), (0,2,1), (1,0,2), (2,1,0)]:
    for p in [(0,1,2), (1,2,0), (2,0,1)]:
        for orientation in [(1, 1, 1), (1, -1, -1), (-1, -1, 1), (-1, 1, -1)]:
            def rotate(beacon):
                beacon = [beacon[i] for i in p]
                return tuple([p*q for p, q in zip(beacon, orientation)])
            yield rotate
    #for p in [(0,2,1), (1,0,2), (2,1,0), (0,1,2), (1,2,0), (2,0,1)]:
    for p in [(0,2,1), (1,0,2), (2,1,0)]:
        for orientation in [(-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]:
            def rotate(beacon):
                beacon = [beacon[i] for i in p]
                return tuple([p*q for p, q in zip(beacon, orientation)])
            yield rotate
assert {frot((1,2,3)) for frot in frotations()} == {
   (1,2,3), (2,3,1), (3,1,2),
   (1,-2,-3), (2,-3,-1), (3,-1,-2),
   (-1,2,-3), (-2,3,-1), (-3,1,-2),
   (-1,-2,3), (-2,-3,1), (-3,-1,2),
   (1,3,-2), (2,1,-3), (3,2,-1),
   (1,-3,2), (2,-1,3), (3,-2,1),
   (-1,3,2), (-2,1,3), (-3,2,1),
   (-1,-3,-2), (-2,-1,-3), (-3,-2,-1),
}


#assert {frot((1,2,3)) for frot in frotations()} == {
#    (1, 2, 3), (-1, 2, 3), (1, -2, 3), (1, 2, -3),
#    (1, 3, 2), (-1, 3, 2), (1, -3, 2), (1, 3, -2),
#    (2, 1, 3), (-2, 1, 3), (2, -1, 3), (2, 1, -3),
#    (2, 3, 1), (-2, 3, 1), (2, -3, 1), (2, 3, -1),
#    (3, 1, 2), (-3, 1, 2), (3, -1, 2), (3, 1, -2),
#    (3, 2, 1), (-3, 2, 1), (3, -2, 1), (3, 2, -1)
#}

def deltas(s1, s2):
    """Generate all possible deltas between the beacons in s1 and s2"""
    for b1 in s1:
        for b2 in s2:
             yield tuple(q-p for p,q in zip(b1,b2))
assert len(list(deltas(test_sensors[0], test_sensors[1]))) == 625

def shift_beacon(b, delta):
    return tuple([p-d for p,d in zip(b, delta)])

#assert shift_beacon((686,422,578), (68,-1246,-43)) == (-618,-824,-621)

def shift_sensor(s, delta):
    return set(shift_beacon(b, delta) for b in s)
# assert shift_sensor({(1,2,3), (4,5,6), (7,8,9)}, (-4,-40,-44)) == {(-3,-38,-41), (0,-35,-38), (3,-32,-35)}

def rotate_sensor(s, frot):
    return set(frot(b) for b in s)

#test_sensors[1]

def sensor_overlaps(s1, s2):
    """If there are overlaps, returns s2's beacons in s1's frame of reference"""
    for frot in frotations():
        rotated2 = rotate_sensor(s2, frot)
        for delta in deltas(s1, rotated2):
            shifted2 = shift_sensor(rotated2, delta)
            overlaps = s1.intersection(shifted2)
            if len(overlaps) >= 12:
                print('Found a match! rotation:', frot((1,2,3)))
                return shifted2, delta
    return set(), None

#sensor_overlaps(test_sensors[0], test_sensors[1])
#sorted(test_sensors[0])
#sorted(shift_sensor(test_sensors[1], (68, -1246, -43)))

#def all_overlaps(sensors):
#    s0 = sensors.pop(0)
#    while len(sensors) > 0:
#        s1 = sensors.pop(0)
#        found = sensor_overlaps(s0, s1)
#        if found:
#            for b in found:
#                s0.add(b)
#        else:
#            # Put it back, but on the end...
#            sensors.append(s1)
#    return s0
#assert len(all_overlaps(parse(test_input))) == 79

def max_manhattans(beacons):
    manhattans = []
    for i in range(len(beacons)-1):
        for j in range(i, len(beacons)):
            manhattans.append(sum(abs(a-b) for a, b in zip(beacons[i], beacons[j])))
    return max(manhattans)

def all_overlaps(sensors):
    dd = []
    done = []
    lucky = []
    unlucky = []
    s0 = sensors.pop(0)
    while True:
        #print('sensors has %d, done has %d, lucky has %d, unlucky has %d' % (len(sensors), len(done), len(lucky), len(unlucky)))
        if len(sensors) == 0:
            if len(unlucky) == 0:
                done += lucky
                done.append(s0)
                break
            done.append(s0)
            s0 = lucky.pop()
            sensors = unlucky
            unlucky = []
        s1 = sensors.pop(0)
        #print('Comparing %s and %s' % (list(s0)[0], list(s1)[0]))
        found, delta = sensor_overlaps(s0, s1)
        # found is s1, but oriented into s0's frame of reference.
        if found:
            #print('Found a match')
            lucky.append(found)
            dd.append(delta)
        else:
            # Put it back, but on the end...
            unlucky.append(s1)
    beacons = set()
    for s in done:
        for b in s:
            beacons.add(b)
    for s in lucky:
        for b in s:
            beacons.add(b)
    #print('Done: sensors has %d, done has %d, lucky has %d, unlucky has %d, beacons has %d' % (len(sensors), len(done), len(lucky), len(unlucky), len(beacons)))
    return beacons, dd
beacons, dd = all_overlaps(parse(test_input))
assert len(beacons) == 79
assert max_manhattans(dd) == 3621

with open('inputs/day19.input') as f:
    sensors = parse(f.read())
    beacons, dd = all_overlaps(sensors)
    print('Day 19, part 1 => %d' % len(beacons))
    print('Day 19, part 2 => %d' % max_manhattans(dd))

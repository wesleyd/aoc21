#!/usr/bin/env python3

from collections import namedtuple

easy_example = """\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""

def parse_line(line):
    outcome, spec = line.split(' ')
    pieces = spec.split(',')
    ret = [outcome]
    for piece in pieces:
        letter, lr = piece.split('=')
        bot, top = lr.split('..')
        ret.append((int(bot), int(top)))
    return tuple(ret)
assert parse_line('off x=9..11,y=11..13,z=-12..7') == ('off', (9,11), (11,13), (-12,7))

def parse(input):
    cubes = set()
    for line in input.splitlines():
        outcome, xx, yy, zz = parse_line(line)
        for x in range(max(-50,xx[0]), min(xx[1],50)+1):
            for y in range(max(-50,yy[0]), min(yy[1], 50)+1):
                for z in range(max(-50,zz[0]), min(zz[1], 50)+1):
                    p = (x,y,z)
                    if outcome == 'on':
                        cubes.add(p)
                    elif outcome == 'off':
                        cubes.discard(p)
                    else:
                        raise Exception('wtf outcome %s in line %s' % (outcome, line))
    return cubes
assert len(parse(easy_example)) == 39

larger_example = """\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""
assert len(parse(larger_example)) == 590784

with open('inputs/day22.input') as f:
    cubes = parse(f.read())
    day22_part1 = len(cubes)
    print('Day 22 part 1 => %d' % day22_part1)

# Day 2

# A range includes lo but not hi
Range = namedtuple('Range', ['lo', 'hi'])

# A Cuboid is just three ranges
Cuboid = namedtuple('Cuboid', ['x', 'y', 'z'])

def make_cuboid(xlo, xhi, ylo, yhi, zlo, zhi):
    return Cuboid(Range(xlo, xhi), Range(ylo, yhi), Range(zlo, zhi))

# A Rule's lit can be 'on' or 'off'.
Rule = namedtuple('Rule', ['lit', 'cuboid'])

def make_rule(lit, xlo, xhi, ylo, yhi, zlo, zhi):
    return Rule(lit, make_cuboid(xlo, xhi, ylo, yhi, zlo, zhi))

def parse_rule(line) -> Rule:
    """turns a string into a Rule"""
    line = line.strip()  # Allow leading spaces
    lit, spec = line.split(' ')
    assert lit in ('on', 'off')
    pieces = spec.split(',')
    letter, lr = pieces[0].split('=')
    assert letter == 'x'
    x1, x2 = lr.split('..')
    letter, lr = pieces[1].split('=')
    assert letter == 'y'
    y1, y2 = lr.split('..')
    letter, lr = pieces[2].split('=')
    assert letter == 'z'
    z1, z2 = lr.split('..')
    return Rule(lit=lit, cuboid=Cuboid(Range(int(x1), int(x2)+1),  # Note the plus ones!
                                       Range(int(y1), int(y2)+1),
                                       Range(int(z1), int(z2)+1)))
assert parse_rule('off x=9..11,y=11..13,z=-12..7') == Rule('off', Cuboid((9,12), (11,14), (-12,8)))
assert parse_rule(' on x=-54112..-39298,y=-85059..-49293,z=-27449..7877') == \
    Rule('on', ((-54112, -39297), (-85059, -49292), (-27449, 7878)))

def parse_rules(input) -> [Rule]:
    rules = []
    for line in input.splitlines():
        rules.append(parse_rule(line))
    return rules
assert parse_rules(easy_example) == [
        Rule('on',  ((10, 13),  (10, 13),  (10, 13))),
        Rule('on',  ((11, 14),  (11, 14),  (11, 14))),
        Rule('off', (( 9, 12),  ( 9, 12),  ( 9, 12))),
        Rule('on',  ((10, 11),  (10, 11),  (10, 11)))]

def contains(c, p):
    """is p in c?"""
    return (c.x.lo <= p[0] and p[0] < c.x.hi and
            c.y.lo <= p[1] and p[1] < c.y.hi and
            c.z.lo <= p[2] and p[2] < c.z.hi)
assert contains(make_cuboid(0,3, 0,3, 0,3), (1,1,1))
assert contains(make_cuboid(0,3, 0,3, 0,3), (0,0,0))
assert not contains(make_cuboid(0,3, 0,3, 0,3), (0,0,3))

def segments(rr: [Range]) -> [Range]:
    pp = []
    for r in rr:
        pp.append(r.lo)
        pp.append(r.hi)
    pp.sort()
    for a, b in zip(pp, pp[1:]):
        if a >= b:
            continue
        yield Range(a,b)
assert list(segments([Range(-20,27), Range(-36,18)])) == [Range(-36,-20), Range(-20,18), Range(18,27)]
assert list(segments([Range(-20,27), Range(-20,27)])) == [Range(-20,27)]
assert list(segments([Range(-20,27), Range(-20,28)])) == [Range(-20,27), Range(27,28)]

def weigh1(c: Cuboid):
    return (c.x.hi - c.x.lo) * (c.y.hi - c.y.lo) * (c.z.hi - c.z.lo)
assert weigh1(make_cuboid(0,3, 0,3, -3,0)) == 27

def is_lit(rules: [Rule], p: tuple) -> bool:
    """returns the litness of the *first* matching rule"""
    for rule in rules:
        if contains(rule.cuboid, p):
            #return rule.lit == 'on'
            if rule.lit == 'on':
                return True
            else:
                return False
    return False

def overlap(r1: Range, r2: Range) -> Range:
    lo, hi = (max(r1.lo, r2.lo), min(r1.hi, r2.hi))
    if lo >= hi:
        return None
    return Range(lo, hi)
assert overlap(Range(1,3), Range(2,4)) == Range(2,3)
assert overlap(Range(2,4), Range(1,3)) == Range(2,3)
assert not overlap(Range(1,2), Range(3,4))
assert not overlap(Range(3,4), Range(1,2))
assert not overlap(Range(1,2), Range(2,3))

def xrules(rules: [Rule], xx: Range):
    """Returns all the rules that might affect xx"""
    matches = []
    for rule in rules:
        if overlap(rule.cuboid.x, xx):
            matches.append(rule)
    return matches

def yrules(rules: [Rule], yy: Range):
    """Returns all the rules that might affect yy"""
    matches = []
    for rule in rules:
        if overlap(rule.cuboid.y, yy):
            matches.append(rule)
    return matches

def weigh(rules):
    n = 0
    rules = rules[::-1]
    for xx in segments([r.cuboid.x for r in rules]):
        xr = xrules(rules, xx)
        for yy in segments([r.cuboid.y for r in xr]):
            yr = yrules(xr, yy)
            for zz in segments([r.cuboid.z for r in yr]):
                p = (xx.lo, yy.lo, zz.lo)
                if is_lit(yr, p):
                #if is_lit(xr, p):
                    r = Cuboid(xx, yy, zz)
                    n += weigh1(r)
    return n
assert weigh(parse_rules("""\
  on x=10..12,y=10..12,z=10..12""")) == 27
assert weigh(parse_rules("""\
  on x=10..12,y=10..12,z=10..12
  on x=11..13,y=11..13,z=11..13""")) == 27 + 19
assert weigh(parse_rules("""\
  on x=10..12,y=10..12,z=10..12
  on x=11..13,y=11..13,z=11..13
  off x=9..11,y=9..11,z=9..11""")) == 27 + 19 - 8
assert weigh(parse_rules("""\
  on x=10..12,y=10..12,z=10..12
  on x=11..13,y=11..13,z=11..13
  off x=9..11,y=9..11,z=9..11
  on x=10..10,y=10..10,z=10..10""")) == 27 + 19 - 8 + 1
assert weigh(parse_rules("""\
  on x=0..3,y=0..3,z=0..0
  on x=2..5,y=2..5,z=0..0""")) == 4*4 + 4*4 - 2*2  # 28
assert weigh(parse_rules("""\
  on x=0..3,y=0..3,z=0..0
  on x=2..5,y=2..5,z=0..0
  on x=3..3,y=3..3,z=0..0""")) == 4*4 + 4*4 - 2*2  # 28  ... the 1x1x1 shouldn't count

def intersection(c1: Cuboid, c2: Cuboid) -> Cuboid:
    ox = overlap(c1.x, c2.x)
    oy = overlap(c1.y, c2.y)
    oz = overlap(c1.z, c2.z)
    if ox and oy and oz:
        return Cuboid(ox, oy, oz)
    return None
assert intersection(make_cuboid(0,2, 0,2, 0,2), make_cuboid(1,3, 1,3, 1,3)) == make_cuboid(1,2, 1,2, 1,2)
assert intersection(make_cuboid(1,3, 1,3, 1,3), make_cuboid(0,2, 0,2, 0,2)) == make_cuboid(1,2, 1,2, 1,2)
assert not intersection(make_cuboid(0,1, 0,2, 0,2), make_cuboid(2,3, 1,3, 1,3))

fifty_fifty = make_cuboid(-50,51, -50,51, -50,51)

def clip_rules(boundary: Cuboid, rr: [Rule]) -> [Rule]:
    result = []
    for r in rr:
        ixn = intersection(boundary, r.cuboid)
        if ixn:
            result.append(Rule(r.lit, ixn))
    return result
assert clip_rules(fifty_fifty, [parse_rule('on x=10..12,y=10..12,z=10..12')]) == [make_rule('on', 10,13, 10,13, 10,13)]
assert clip_rules(fifty_fifty, [parse_rule('on x=-54112..-39298,y=-85059..-49293,z=-27449..7877')]) == []

assert weigh(clip_rules(fifty_fifty, parse_rules(larger_example)))  == 590784

huge_example = """\
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""
assert weigh(clip_rules(fifty_fifty, parse_rules(huge_example))) == 474140
assert weigh(parse_rules(huge_example)) == 2758514936282235

with open('inputs/day22.input') as f:
    assert weigh(clip_rules(fifty_fifty, parse_rules(f.read()))) == day22_part1

with open('inputs/day22.input') as f:
    print('Day 22 part 2 => %d' % weigh(parse_rules(f.read())))

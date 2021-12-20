#!/usr/bin/env python3

from dataclasses import dataclass

test_input = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""

@dataclass
class Image:
    data: dict
    background: str
    def at(self, x: int, y :int):
        return self.data.get((x,y), self.background)

def parse_algo(input: str):
    first, _ = input.split('\n\n')
    return ''.join(first.splitlines())
assert len(parse_algo(test_input)) == 512

def parse_image(input: str):
    first, rest = input.split('\n\n')
    background = '.'
    data = {}
    for y, line in enumerate(rest.splitlines()):
        for x, c in enumerate(line):
            data[(x,y)] = c
    image = Image(data, background)
    return image
assert parse_image(test_input).at(0,0) == '#'
assert parse_image(test_input).at(-1000,-10000) == '.'

def nlit(image: Image):
    if image.background == '#':
        return float('inf')
    return sum([1 if c == '#' else 0 for c in image.data.values()])
assert nlit(parse_image(test_input)) == 10

def bounds(image: Image):
    left, right, top, bottom = 0, 0, 0, 0
    for x,y in image.data.keys():
        if x < left:
            left = x
        if x+1 > right:
            right = x+1
        if y < top:
            top = y
        if y+1 > bottom:
            bottom = y+1
    return (left, right, top, bottom)
assert bounds(parse_image(test_input)) == (0, 5, 0, 5)

def resolve(image: Image, x: int, y: int):
    cc = [
        image.at(x-1, y-1), image.at(x, y-1), image.at(x+1,y-1),
        image.at(x-1, y),   image.at(x, y),   image.at(x+1,y),
        image.at(x-1, y+1), image.at(x, y+1), image.at(x+1,y+1),
    ]
    s = ''.join(cc)
    return int(s.replace('#', '1').replace('.', '0'), 2)
assert resolve(parse_image(test_input), 2, 2) == 34

def strimage(image: Image):
    left, right, top, bottom = bounds(image)
    lines = []
    for y in range(top, bottom):
        line = []
        for x in range(left, right):
            line.append(image.at(x, y))
        lines.append(''.join(line))
    return '\n'.join(lines)
assert strimage(parse_image(test_input)) == """\
#..#.
#....
##..#
..#..
..###"""

def enhance(before: Image, algo: list):
    left, right, top, bottom = bounds(before)
    data = {}
    for y in range(top-1, bottom+1):
        for x in range(left-1, right+1):
            r = resolve(before, x, y)
            data[(x,y)] = algo[r]
    r = resolve(before, float('inf'), float('inf'))
    background = algo[resolve(before, float('inf'), float('inf'))]
    return Image(data, background)
assert (strimage(enhance(parse_image(test_input), parse_algo(test_input)))) == """\
.##.##.
#..#.#.
##.#..#
####..#
.#..##.
..##..#
...#.#."""

def enhanceN(img: Image, algo: list, n: int):
    for i in range(n):
        img = enhance(img, algo)
    return img
assert strimage(enhanceN(parse_image(test_input), parse_algo(test_input), 2)) == """\
.......#.
.#..#.#..
#.#...###
#...##.#.
#.....#.#
.#.#####.
..#.#####
...##.##.
....###.."""

with open('inputs/day20.input') as f:
    day20_input = f.read()
    day20_algo = parse_algo(day20_input)
    day20_image = parse_image(day20_input)
    day20_after2 = enhanceN(day20_image, day20_algo, 2)
    print('Day 20 part 1 => %d' % nlit(day20_after2))

# Part 2

assert nlit(enhanceN(parse_image(test_input), parse_algo(test_input), 50)) == 3351
with open('inputs/day20.input') as f:
    day20_input = f.read()
    day20_algo = parse_algo(day20_input)
    day20_image = parse_image(day20_input)
    day20_after50 = enhanceN(day20_image, day20_algo, 50)
    print('Day 20 part 2 => %d' % nlit(day20_after50))



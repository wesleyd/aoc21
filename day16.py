#!/usr/bin/env python3

import math

def hex_to_bits(h):
    """returns turns nybbles in a string into bits in a string, pads properly"""
    return ''.join(['{0:04b}'.format(int(nybble, 16)) for nybble in h])

assert hex_to_bits("0A") == '00001010'
assert hex_to_bits("38006F45291200") == '00111000000000000110111101000101001010010001001000000000'

def nbits(n, bits):
    """nbits takes n bits from bits and returns it, and the rest"""
    return bits[0:n], bits[n:]

def parse_literal(bits):
    """Extract a literal number from bits, and return it, and the rest."""
    n = 0
    while True:
        chunk = bits[0:5]
        bits = bits[5:]
        m = int(chunk[1:], 2)
        n = (n << 4) + m
        if chunk[0] == '0':
            return n, bits

def parse_packet_internal(bits, indent):
    """like parse_packet, but takes a bitstring, and returns remainder"""
    #print('%sparsing packet with %d bits' % (indent, len(bits)))
    packet = {}
    s, bits = nbits(3, bits)
    packet['V'] = int(s,2)
    #print('%s packet version is %d (%s)' % (indent, packet['V'], s))
    s, bits = nbits(3, bits)
    packet['T'] = int(s,2)
    #print('%s packet type is %d (%s)' % (indent, packet['T'], s))
    if packet['T'] == 4:  # Literal 
        #print('%s literal packet' % indent)
        packet['LITERAL'], bits = parse_literal(bits)
    else:  # Operator packet
        #print('%s operator packet' % indent)
        l, bits = nbits(1, bits)
        l = int(l,2)
        packet['PACKETS'] = []
        if l == 0:  # some number of bits worth of packets
            bb, bits = nbits(15, bits)
            nb = int(bb, 2)
            #print('%s length zero => packets in %d (%s) bits' % (indent,  nb, bb))
            data, bits = nbits(nb, bits)
            while len(data) > 0:
                p, data = parse_packet_internal(data, indent=indent+'  ')
                packet['PACKETS'].append(p)
        elif l == 1:  # some number of packets
            bb, bits = nbits(11, bits)
            np = int(bb, 2)
            #print('%s length one => %d (%s) packets' % (indent, np, bb))
            for i in range(np):
                p, bits = parse_packet_internal(bits, indent=indent+'  ')
                packet['PACKETS'].append(p)
        else:
            raise Exception('Unknown l %r' % l)
    return packet, bits

def parse_packet(h, indent=''):
    p, rest = parse_packet_internal(hex_to_bits(h), indent)
    if len(rest) > 0:
        z = int(rest, 2)
        if z != 0:
            raise Exception('bad remainder %d/%s, not zero' % (z, rest))
    return p

assert parse_packet('D2FE28')['LITERAL'] == 2021

parse_packet('38006F45291200')

parse_packet('EE00D40C8230600')

def add_up_version_numbers(p):
    v = p['V']
    for q in p.get('PACKETS', []):
        v += add_up_version_numbers(q)
    return v

assert add_up_version_numbers(parse_packet('8A004A801A8002F478')) == 16
assert add_up_version_numbers(parse_packet('620080001611562C8802118E34')) == 12
assert add_up_version_numbers(parse_packet('C0015000016115A2E0802F182340')) == 23
assert add_up_version_numbers(parse_packet('A0016C880162017C3686B18A3D4780')) == 31

with open('inputs/day16.input') as f:
    p = parse_packet(f.read().strip())
    vv = add_up_version_numbers(p)
    print('Day 16 part 1 => %d' % vv)

### Part 2

def apply(p):
    if p['T'] == 4:   # literal packet
        return p['LITERAL']
    elif p['T'] == 0:   # sum
        return sum([apply(q) for q in p['PACKETS']])
    elif p['T'] == 1:  # product
        return math.prod([apply(q) for q in p['PACKETS']])
    elif p['T'] == 2:  # mininmum
        return min([apply(q) for q in p['PACKETS']])
    elif p['T'] == 3:  # mininmum
        return max([apply(q) for q in p['PACKETS']])
    elif p['T'] == 5:  # greater than
        pp = p['PACKETS']
        if apply(pp[0]) > apply(pp[1]):
            return 1
        return 0
    elif p['T'] == 6:  # less than
        pp = p['PACKETS']
        if apply(pp[0]) < apply(pp[1]):
            return 1
        return 0
    elif p['T'] == 7:  # equal
        pp = p['PACKETS']
        if apply(pp[0]) == apply(pp[1]):
            return 1
        return 0
    else:
        raise Exception('unknown packet type %d' % p['T'])

assert apply(parse_packet('C200B40A82')) == 3
assert apply(parse_packet('04005AC33890')) == 54
assert apply(parse_packet('880086C3E88112')) == 7
assert apply(parse_packet('CE00C43D881120')) == 9
assert apply(parse_packet('D8005AC2A8F0')) == 1
assert apply(parse_packet('F600BC2D8F')) == 0
assert apply(parse_packet('9C005AC2F8F0')) == 0
assert apply(parse_packet('9C0141080250320F1802104A08')) == 1

with open('inputs/day16.input') as f:
    p = parse_packet(f.read().strip())
    x = apply(p)
    print('Day 16 part 2 => %d' % x)

#!/usr/bin/env python3

day3_test_input = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]

def power(inputs):
    γ = ""
    Ɛ = ""
    for i in range(len(inputs[0])):
        ones = 0
        zeros = 0
        for s in inputs:
            if s[i] == '1':
                ones += 1
            else:
                zeros += 1
        if ones == zeros:
            raise Exception('same number of ones as zeros, bit %d, %d==%d', i, ones, zeros)
        if ones > zeros:
            γ += '1'
            Ɛ += '0'
        else:
            γ += '0'
            Ɛ += '1'
    return int(γ,2) * int(Ɛ,2)

with open("day03.input") as f:
    day3_input = f.read().splitlines()

day3a = power(day3_input)
print("Day 3 Part 1 =>", day3a)  # => 3985686

#### Part 2

def popularity_split(lst, digit):
    """Split lst into two lists on digit-th digit, more popular first"""
    ones, zeros = [], [] 
    for s in lst:
        if s[digit] == '1':
            ones.append(s)
        else:
            zeros.append(s)
    if len(zeros) > len(ones):
        return zeros, ones
    return ones, zeros

def oxygen(lst):
    i = 0
    while len(lst) > 1 and i < len(lst[0]):
        lst, _ = popularity_split(lst, i)
        i += 1
    return int(lst[0], 2)

def co2(lst):
    i = 0
    while len(lst) > 1 and i < len(lst[0]):
        _, lst = popularity_split(lst, i)
        i += 1
    return int(lst[0], 2)

def life_support(lst):
    return oxygen(lst) * co2(lst)

got = life_support(day3_test_input)
if got != 230:
    raise Exception('life_support on test input got %d want %d' % (got, 230))

day3b = life_support(day3_input)
print("Day 3 Part 2 =>", day3b)  # => 2555739

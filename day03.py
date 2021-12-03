#!/usr/bin/env python

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
    day3a = power(f.read().splitlines())
    print("Day 3 Part 1 =>", day3a)  # => 3985686

####

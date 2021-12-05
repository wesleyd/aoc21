#!/usr/bin/env python

day4_test_input = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

class Card:
    """A Card is a bingo card."""
    def __init__(self, input):
        self.numbers = []
        for line in input.splitlines():
            self.numbers.append(list(map(int, line.split())))
    def play1(self, ball):
        for i in range(len(self.numbers)):
            for j in range(len(self.numbers[i])):
                if self.numbers[i][j] == ball:
                    # Let's negate played numbers
                    self.numbers[i][j] *= -1
    def bingo(self):
        """Returns true if this card has won."""
        diagonal = []
        for i in range(len(self.numbers)):
            diagonal.append(self.numbers[i][i])
        

class Game:
    """A Game is, like, a whole game of bingo."""
    def __init__(self, input):
        pieces = input.split('\n\n')
        self.balls = list(map(int, pieces[0].split(',')))
        self.cards = list(map(Card, pieces[1:]))
    def play1(self):
        ball = self.balls.pop(0)
        for card in self.cards:
            if 


g = Game(day4_test_input)


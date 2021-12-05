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

def negative(x):
    return x < 0

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
                    # Let's just set played numbers to -1
                    self.numbers[i][j] = -1
    def bingo(self):
        """Returns true if this card has won."""
        for row in self.numbers:
            if all(negative(x) for x in row):
                return True
        for j in range(len(self.numbers[0])):
            vertical = []
            for i in range(len(self.numbers)):
                vertical.append(self.numbers[i][j])
            if all(negative(x) for x in vertical):
                return True
        diagonal = []
        for i in range(len(self.numbers)):
            diagonal.append(self.numbers[i][i])
        if all(negative(x) for x in diagonal):
            return True
    def unmarked_sum(self):
        """Sum of all the ummarked numbers on the card"""
        sum = 0
        for row in self.numbers:
            for n in row:
                if n > 0:
                    sum += n
        return sum
        

class Game:
    """A Game is, like, a whole game of bingo."""
    def __init__(self, input):
        pieces = input.split('\n\n')
        self.balls = list(map(int, pieces[0].split(',')))
        self.cards = list(map(Card, pieces[1:]))
    def play(self):
        for ball in self.balls:
            print("Playing ball", ball)
            for card in self.cards:
                card.play1(ball)
                if card.bingo():
                    sum = card.unmarked_sum()
                    score = ball * sum
                    print("%d * %d = %d" % (ball, sum, score))
                    return score

g = Game(day4_test_input)
got = g.play()
if got != 4512:
    raise Exception('Got %d want 4512' % got)

with open("day04.input") as f:
    day4_input = f.read()
    g = Game(day4_input)
    score = g.play()
    print("Day 4 Part 1 =>", score) # 41668

### Part 2 :: let the squid win!

def print_cards(cards):
    idx = -1
    for i in range(len(cards)):
        if cards[i] is not None:
            idx = i
            break
    print('First non-null card is %d'%idx)
    if idx == -1:
        return
    for row in range(len(cards[idx].numbers)):
        for card in cards:
            if not card:
                print(21*' ', end='')
                continue
            for n in card.numbers[row]:
                if n < 0:
                    print(' XX ', end='')
                else:
                    print('%3d ' % n, end='')
            print('  ', end='')
        print()

def play_badly(game):
    last_ball = -1
    last_sum = -1
    print_cards(game.cards)
    for ball in game.balls:
        print("Playing ball (badly)", ball)
        for c in range(len(game.cards)):
            card = game.cards[c]
            if not card:
                continue
            card.play1(ball)
            if card.bingo():
                print('Card %d has won!' % c)
                game.cards[c] = None
                last_ball = ball
                last_sum = card.unmarked_sum()
        print_cards(game.cards)
        if not any(game.cards):
            print('No cards left.')
            break
    return last_ball * last_sum

g = Game(day4_test_input)
got = play_badly(g)
if got != 1924:
    raise Exception('Got %d want 1924' % got)

with open("day04.input") as f:
    day4_input = f.read()
    g = Game(day4_input)
    score = play_badly(g)
    print("Day 4 Part 2 =>", score)  # 10478



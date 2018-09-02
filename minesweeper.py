import random
from datetime import datetime

CHAR_CLOSED = '.'
CHAR_BOMB = '*'
CHAR_EMPTY = '_'

TYPE_EMPTY = 0
TYPE_BOMB = -1

STATUS_IDLE = 0
STATUS_WINNING = 1
STATUS_LOSING = 2


class Minesweeper(object):

    def __init__(self, n, b):
        self.n = n
        self.b = b
        self.board = []
        self.opened = []
        self.bombCoordinates = []

        for i in range(n):
            self.board.append([TYPE_EMPTY] * n)
            self.opened.append([False] * n)

        # generate bombs in the board
        random.seed(datetime.now())
        remainingBombs = self.b
        while remainingBombs > 0:
            x, y = random.randint(0, self.n-1), random.randint(0, self.n-1)
            if not self.isBomb(x, y):
                self.board[x][y] = TYPE_BOMB
                self.bombCoordinates.append((x,y))
                remainingBombs -= 1

        # all complete: bombs are set
        # the next step is to insert number indicators
        self.setNumberIndicators()

    def setNumberIndicators(self):
        for i in range(len(self.bombCoordinates)):
            x, y = self.bombCoordinates[i]
            self.incrementNearbyColumsToBombs(x, y)

    def incrementNearbyColumsToBombs(self, x, y):
        counter = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.n) and (0 <= j < self.n) and (x != i or y != j) and not self.isBomb(i, j):
                    self.board[i][j] += 1

        return counter

    def start(self):
        status = STATUS_IDLE

        self.printBombsOnly()

        while status == STATUS_IDLE:
            self.printBoard()
            y, x = map(int, input().split())

            if (0 <= x < self.n) and (0 <= y < self.n):
                if self.checkClickedPoint(x, y):
                    if self.isGameFinished():
                        status = STATUS_WINNING
                else:
                    status = STATUS_LOSING
            else:
                print("Validation: x and y point must be between 0 and n (={})".format(self.n))

        self.printBoard()

    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.opened[i][j]:
                    print(self.getStringRepr(i, j), end=' ')
                else:
                    print(CHAR_CLOSED, end=' ')
    
            print()
        print()

    def printOpenedBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.getStringRepr(i, j), end=' ')
    
            print()
        print()
    
    def printBombsOnly(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.isBomb(i, j):
                    print(CHAR_BOMB, end=' ')
                else:
                    print(CHAR_CLOSED, end=' ')
    
            print()
        print()

    def getStringRepr(self, i, j):
        if self.board[i][j] == TYPE_BOMB:
            return CHAR_BOMB
        elif self.board[i][j] == TYPE_EMPTY:
            return CHAR_EMPTY
        else:
            return str(self.board[i][j])

    def checkClickedPoint(self, x, y):
        if not self.opened[x][y]:
            if self.isBomb(x, y):
                self.openAllBombs()
                return False
            else:
                self.open(x, y)
                return True

        return True

    def openAllBombs(self):
        for p in self.bombCoordinates:
            self.opened[p[0]][p[1]] = True

    def open(self, x, y):
        if 0 <= x < self.n and 0 <= y < self.n:
            if not self.opened[x][y]:
                self.opened[x][y] = True

                if self.isEmpty(x, y):
                    self.open(x-1, y-1)
                    self.open(x-1, y)
                    self.open(x-1, y+1)
                    self.open(x, y-1)
                    self.open(x, y+1)
                    self.open(x+1, y-1)
                    self.open(x+1, y)
                    self.open(x+1, y+1)

    def isBomb(self, x, y):
        return self.board[x][y] == TYPE_BOMB

    def isEmpty(self, x, y):
        return self.board[x][y] == TYPE_EMPTY

    def isGameFinished(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if not self.opened[i][j] and not self.isBomb(i, j):
                    return False
        
        return True


def main():
    n = int(input())
    b = int(input())

    game = Minesweeper(n, b)
    game.start()


if __name__ == '__main__':
    main()
import pygame as py
import sys
import numpy
import tkinter as tk
from tkinter import messagebox
py.init()

# display
width = 640
height = 560
win = py.display.set_mode((width, height))
py.display.set_caption('CONNECT 4 ^_^')


# colors
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 250, 250)
nokia = (178, 189, 8)
yellow = (255, 217, 15)
wood = (133, 94, 66)

# grid
row = 6
column = 7
rectgrid = [py.draw.rect(win, blue, (i * 90, j * 90, 90, 90))
            for i in range(column) for j in range(row)]
circlegrid1 = []
circlegrid2 = []


def grid(win, row, column):
    sep = 90

    for i in range(column+1):
        py.draw.line(win, blue, (i * sep, 0), (i * sep, 543), 7)
    for i in range(row+1):
        py.draw.line(win, blue, (0, i * sep), (627, i * sep), 7)
    for i in range(column):
        for j in range(row):
            py.draw.circle(win, black, ((i * 90) + 45, (j * 90) + 45), 45 - 7)
    for (i, j) in circlegrid1:
        py.draw.circle(win, red, ((i * 90) + 45, (j * 90) + 45), 45 - 7)
    for (i, j) in circlegrid2:
        py.draw.circle(win, yellow, ((i * 90) + 45, (j * 90) + 45), 45 - 7)

# items


class Player:
    def __init__(self, color, turn):
        self.color = color
        self.turn = turn
        self.moves = set({})

    def is_winner(self):
        for i in range(3):
            for j in range(7):
                if (((i, j) in self.moves) and ((i + 1, j) in self.moves) and ((i + 2, j) in self.moves) and ((i + 3, j) in self.moves)):
                    return True
        for i in range(6):
            for j in range(4):
                if (((i, j) in self.moves) and ((i, j+1) in self.moves) and ((i, j+2) in self.moves) and ((i, j+3) in self.moves)):
                    return True
        for i in range(3):
            for j in range(3):
                if (((i, j) in self.moves) and ((i+1, j+1) in self.moves) and ((i+2, j+2) in self.moves) and ((i+3, j+3) in self.moves)):
                    return True
        for i in range(3):
            for j in range(6, 2, -1):
                if (((i, j) in self.moves) and ((i+1, j-1) in self.moves) and ((i+2, j-2) in self.moves) and ((i+3, j-3) in self.moves)):
                    return True
        return False


class Game:
    def __init__(self):
        self.available = numpy.zeros((6, 7))
        for i in range(7):
            self.available[5, i] = 1

    def isdrow(self):
        for i in range(6):
            for j in range(7):
                if self.available[i, j] == 1:
                    return False
        return True


# redraw function
def redraw(win):
    win.fill(blue)
    grid(win, row, column)

    py.display.update()


# instences
player1 = Player(red, True)
player2 = Player(yellow, False)
game = Game()

# rest function


def reset(p1, p2, g):
    p1.turn = True
    p2.turn = False
    g.available = numpy.zeros((6, 7))
    for i in range(7):
        g.available[5, i] = 1
    p1.moves = set({})
    p2.moves = set({})
    global circlegrid1
    circlegrid1 = []
    global circlegrid2
    circlegrid2 = []


# message box UI
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


# main loop
while 1:

    if not player1.is_winner() and not player2.is_winner() and not game.isdrow():
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit(0)
        # commands
            for rect in rectgrid:
                if event.type == py.MOUSEBUTTONUP and rect.collidepoint(py.mouse.get_pos()):
                    if game.available[rect[1] // 90, rect[0] // 90] == 1:
                        if player1.turn:
                            circlegrid1.append((rect[0] // 90, rect[1] // 90))
                            player1.turn = False
                            player2.turn = True
                            player1.moves.add((rect[1] // 90, rect[0] // 90))
                            game.available[rect[1] // 90, rect[0] // 90] = 0
                            if (rect[1] // 90) > 0:
                                game.available[(rect[1] // 90) - 1,
                                               rect[0] // 90] = 1
                        elif player2.turn:
                            circlegrid2.append((rect[0] // 90, rect[1] // 90))
                            player2.turn = False
                            player1.turn = True
                            player2.moves.add((rect[1] // 90, rect[0] // 90))
                            game.available[rect[1] // 90, rect[0] // 90] = 0
                            if (rect[1] // 90) > 0:
                                game.available[(rect[1] // 90) - 1,
                                               rect[0] // 90] = 1

    else:
        reset(player1, player2, game)

    # game result
    if (player1.is_winner()):
        message_box('RED Wins!', 'Play again...')
    elif player2.is_winner():
        message_box('YELLOW Wins!', 'Play again...')
    elif game.isdrow():
        message_box("It's a Drow!", 'Play again...')

    redraw(win)


############################ done for now needs better graphics and SFX ############################

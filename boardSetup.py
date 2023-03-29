# Sets up the board
import turtle, helper
from typing import List, Tuple

def pen(sol: str) -> turtle.Turtle:
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    message(pen, '1', -448, 310, True)
    message(pen, sol, 0, -360, False, 10)
    return pen

def message(pen: turtle.Turtle, text: str, x: int, y: int, title: bool, size: int = 12, pivot: str = "center") -> None:
    pen.setposition(x, y)
    if title:
        pen.write(text, True, align = pivot, font = ("Arial", size + 6, "bold"))
    else:
        pen.write(text, True, align = pivot, font = ("Arial", size, "normal"))

def rect(obj: turtle.Turtle, x: int, y: int, w: int, h: int) -> None:
    obj.setposition(x, y)
    obj.begin_fill()
    obj.pendown()
    for i in range(2):
        obj.forward(w)
        obj.left(90)
        obj.forward(h)
        obj.left(90)
    obj.penup()
    obj.end_fill()

def triangle(obj: turtle.Turtle, x: int, y: int, size: int) -> None:
    obj.setposition(x, y)
    obj.begin_fill()
    obj.pendown()
    for i in range(3):
        obj.forward(size)
        obj.right(120)
    obj.penup()
    obj.end_fill()

# Create board turtle
def setupBoard(x:int, y:int, scale: int, title: str, screen: turtle.Screen) -> turtle.Turtle:
    board = turtle.Turtle()
    # Store board variables for future use
    board.x = x
    board.y = y
    board.scale = scale
    # Draw the board
    board.color("black", "gray")
    board.penup()
    board.setposition(x, y)
    message(board, title, x, y + scale * 3 + scale / 2, True, 6, "left")
    board.pendown()
    # 6x6 grid (80x80 squares)
    for i in range(6):
        for j in range(6):
            rect(board, x + i * scale, y + j * scale - scale * 3, scale, scale)
    # Draw surrounding board
    board.color("black", "dark gray")
    board.setposition(x + scale * 6, y + scale)
    board.pendown()
    board.begin_fill()
    board.left(90)
    board.forward(scale * 2)
    for i in range(3):
        board.left(90)
        board.forward(scale * 6)
    board.left(90)
    board.forward(scale * 3)
    board.right(90)
    board.forward(scale / 2)
    board.right(90)
    board.forward(scale * 3 + scale / 2)
    for i in range(3):
        board.right(90)
        board.forward(scale * 7)
    board.right(90)
    board.forward(scale * 3 - scale / 2)
    board.right(90)
    board.forward(scale / 2)
    board.end_fill()
    # Draw exit arrow for carpark
    board.penup()
    board.right(90)
    triangle(board, x + scale * 6 + scale / 4, y + scale / 4, scale / 2)
    board.hideturtle()
    return board

def vehicle(shape: str) -> turtle.Turtle:
    vehicle = turtle.Turtle()
    vehicle.penup()
    vehicle.shape(shape)
    vehicle.hideturtle()
    return vehicle

def menu() -> turtle.Turtle:
    menu = turtle.Turtle()
    menu.color("black", "gray")
    menu.penup()
    menu.setposition(-175, 300)
    menu.write("RUSH HOUR", True, align = "center", font = ("Arial", 36, "bold"))
    rect(menu, 40, 300, 160, 60)
    message(menu, "SOLVE", 120, 315, True)
    rect(menu, 220, 300, 160, 60)
    message(menu, "RUN ALL", 300, 315, True)
    message(menu, "(saves to file)", 300, 300, False)
    rect(menu, 400, 300, 160, 60)
    message(menu, "QUIT", 480, 315, True)
    rect(menu, -475, 300, 50, 50)
    menu.left(90)
    triangle(menu, -400, 300, 50)
    menu.left(180)
    triangle(menu, -500, 350, 50)
    menu.hideturtle()
    return menu

def updatePen(pen: turtle.Turtle, x: int, y: int, num: int, out: str) -> None:
    pen.clear()
    message(pen, num, x, y, True)
    if len(out) > 159:
        message(pen, out[:159], 0, -345, False, 10)
        message(pen, out[159:], 0, -360, False, 10)
    else:
        message(pen, out, 0, -360, False, 10)

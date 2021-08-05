import turtle
from math import *

k = 40
t = turtle.Turtle()
t.hideturtle()
t.dot()


def skip(x, y, degree):
    t.penup()
    t.goto(x, y)
    t.setheading(180 * degree / pi)
    t.pendown()


def main():
    skip(4 * k * cos(pi / 8), 4 * k * sin(pi / 8), pi / 2)
    t.pensize(10)
    for i in range(7):
        t.left(45)
        t.forward(3 * k)
    t.pensize(6)
    skip(-0.4 * k, -(3 / sqrt(2) + 1.5) * k, pi / 2)
    t.forward((3 / sqrt(2) + 1.5 - 0.4) * k)
    t.circle(-0.4 * k, 90)
    t.pensize(8)
    t.pencolor("blue")
    t.forward(0.8 * k)
    t.left(90)
    t.circle(0.8 * k, 270)
    t.pencolor("black")
    t.pensize(6)
    t.circle(-0.4 * k, 90)
    t.forward((3 / sqrt(2) + 1.5 - 1.2) * k)
    t.pensize(10)
    for i in range(3):
        skip(1.5 * k, -(4 + 0.6 * i) * k, pi)
        t.forward(3 * k)
    t.setheading(90)
    t.forward(1.2 * k)
    skip(1.5 * k, -5.8 * k, -pi / 2)
    t.fillcolor("black")
    t.begin_fill()
    t.circle(-1.5 * k, 180)
    t.right(90)
    t.forward(3 * k)
    t.end_fill()
    for i in range(3):
        skip(((1.4 + 0.6 * i) * k) * cos(pi / 6), ((1.4 + 0.6 * i) * k) * sin(pi / 6), 2 * pi / 3)
        t.circle((1.4 + 0.6 * i) * k, 120)
    turtle.done()


if __name__ == "__main__":
    main()

import turtle
import math as m

pi = 3.1415926535898
k = 13
r = 30
R = r * m.tan(pi / k)

t = turtle.Turtle()


def leaf(radius):
    t.begin_fill()
    t.fillcolor('green')
    t.right(90)
    t.circle(radius, 90)
    t.left(90)
    t.circle(radius, 90)
    t.end_fill()
    t.pu()
    t.bk(radius)
    t.left(90)
    t.fd(radius)
    t.right(135)
    t.pd()
    t.fd(radius * (2 ** 0.5))
    t.right(135)


def pot(para):
    t.begin_fill()
    t.fillcolor('brown')
    t.left(90)
    t.fd(para)
    Angle = (180 / pi) * m.acos(2 / 7)
    t.right(180 - Angle)
    t.fd((7 / 5) * para)
    t.right(Angle)
    t.fd((6 / 5) * para)
    t.right(Angle)
    t.fd((7 / 5) * para)
    t.right(180 - Angle)
    t.fd(para)
    t.right(90)
    t.end_fill()


t.hideturtle()
t.seth(-90)
t.fillcolor('red')
for i in range(k):
    t.begin_fill()
    t.fd(r)
    t.circle(R, 180 * (1 + 2 / k))
    t.fd(r)
    t.left(180)
    t.end_fill()
t.pu()
t.fd(2 * r / 3)
t.pd()
t.left(90)
t.fillcolor('yellow')
t.begin_fill()
t.circle(2 * r / 3, 360)
t.end_fill()
t.right(90)
t.pu()
t.fd(r / 3)
t.pd()
t.fd(50)
t.left(180)
leaf(35)
t.left(90)
leaf(35)
t.left(90)
t.fd(30)
pot(30)

turtle.done()

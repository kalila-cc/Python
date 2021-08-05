import turtle
import time

r = 150
hr = 60
mr = 80
sr = 110

t = turtle.Turtle()
t.hideturtle()
t.speed(0)


def cut(R, short, deg):
    t.pu()
    t.fd(R - short)
    t.pd()
    t.fd(short)
    t.left(90)
    t.pu()
    t.circle(R, deg)
    t.right(90)
    t.bk(R)
    t.pd()


def pan():
    t.pu()
    t.fd(r)
    t.pd()
    t.left(90)
    t.circle(r, 360)
    t.right(90)
    t.pu()
    t.bk(r)
    t.dot(4)


def scale():
    t.seth(0)
    for i in range(4):
        t.pensize(4)
        cut(r, 4, 6)
        for j in range(3):
            t.pensize(2)
            for k in range(4):
                cut(r, 2, 6)
            t.pensize(3)
            cut(r, 3, 6)
        cut(r, 0, -6)


def dr(length):
    t.pu()
    t.fd(length)
    t.pd()
    t.bk(length)


def dhr():
    t.pensize(5)
    dr(hr)


def dmr():
    t.pensize(3)
    dr(mr)


def dsr():
    t.pensize(1)
    dr(sr)


def show():
    pan()
    scale()
    ti = time.localtime()
    second = ti[5]
    minute = ti[4]
    hour = ti[3] + minute / 60
    t.seth(90 - hour * 30)
    dhr()
    t.seth(90 - 6 * minute)
    dmr()
    t.seth(90 - 6 * second)
    dsr()
    t.pu()
    t.goto(-r / 6, -2 * r / 3)
    newhour = ti[3]
    if ti[3] > 12:
        newhour = ti[3] - 12
    st = f"time: {newhour:02d}:{ti[4]:02d}:{ti[5]:02d}"
    t.write(st, 15)


while True:
    t.home()
    show()
    time.sleep(3)
    t.clear()

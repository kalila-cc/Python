import turtle

t = turtle.Turtle()

t.ht()
t.pu()
t.bk(100)
t.left(90)
t.fd(100)
t.right(90)
t.pd()
t.speed(0)


def koch(level, length):
    if level == 0:
        t.fd(length)
    else:
        koch(level - 1, length / 3)
        t.left(60)
        koch(level - 1, length / 3)
        t.right(120)
        koch(level - 1, length / 3)
        t.left(60)
        koch(level - 1, length / 3)


def Koch(level, line):
    for i in range(3):
        koch(level, line)
        t.right(120)


Koch(3, 300)

turtle.done()

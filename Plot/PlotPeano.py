import turtle

t = turtle.Turtle()

dist = 256
t.ht()
t.pu()
t.goto(-dist / 2, -dist / 2)
static_level = 3
t.speed(0)
t.pd()


def cut():
    global dist, static_level
    return dist / (2 ** (2 + static_level) - 1)


fd = cut()


def fdtn(des, reverse=False):
    if reverse:
        t.right(90 * des)
        t.fd(fd)
    else:
        t.fd(fd)
        t.right(90 * des)


def sunit(flag):
    fdtn(1 * flag)
    fdtn(1 * flag)
    fdtn(-1 * flag)
    fdtn(0)
    fdtn(-1 * flag)
    fdtn(-1 * flag)
    fdtn(1 * flag)
    fdtn(1 * flag)
    fdtn(-1 * flag)
    fdtn(-1 * flag)
    fdtn(0)
    fdtn(-1 * flag)
    fdtn(1 * flag)
    fdtn(1 * flag)
    fdtn(0)


def unit(flag):
    sunit(1 * flag)
    fdtn(1 * flag)
    sunit(-1 * flag)
    fdtn(0)
    sunit(-1 * flag)
    fdtn(1 * flag, True)
    sunit(1 * flag)


def Peano(level, flag):
    if level == 1:
        unit(flag)
    else:
        if level % 2 == 0:
            Peano(level - 1, flag)
            fdtn(-flag, True)
            Peano(level - 1, -flag)
            fdtn(flag, True)
            t.right(90 * flag)
            Peano(level - 1, -flag)
            fdtn(-flag)
            Peano(level - 1, flag)
        else:
            Peano(level - 1, flag)
            fdtn(flag)
            Peano(level - 1, -flag)
            fdtn(0)
            Peano(level - 1, -flag)
            fdtn(flag, True)
            Peano(level - 1, flag)


Peano(static_level, -1)

turtle.done()

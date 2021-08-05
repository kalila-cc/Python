import turtle

t = turtle.Turtle()
t.hideturtle()
r = 20
d = r * (2 ** 0.5 + 1)
t.pencolor('black')
t.pensize(2)

for j in range(4):
    t.begin_fill()
    t.fd(d)
    t.circle(r, 225)
    t.left(180)
    t.circle(r, 225)
    t.fd(d)
    t.left(180)
    t.fillcolor('green')
    t.end_fill()

t.pu()
t.goto(-15, 150)
t.write('clover', 40)

turtle.done()

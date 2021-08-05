import turtle

t = turtle.Turtle()
t.hideturtle()
r = 4
k = 3
t.pencolor('brown')
t.pensize(2 * r)
for i in range(2 * k):
    t.fd(20 * k - 10 * i)
    t.circle(r * pow(-1, i), 180)
for i in range(18):
    t.circle(r, 10)
    t.pensize(2 * r * (1 - i / 18))

turtle.done()

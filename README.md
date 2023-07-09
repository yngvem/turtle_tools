# Simple utilities that extend the Turtle module

This code extends the `turtle` module with context managers for the following tasks:

 * `turtle.penup`
 * `turtle.pendown`
 * `turtle.color`
 * `turtle.pencolor`
 * `turtle.fillcolor`
 * `turtle.speed`
 * `turtle.fill`
 * `turtle.poly`
 * `turtle.pensize`
 * `disable_autoupdate`
 * `enable_autoupdate`

In addition to a `save_postscript` function to save the current canvas as an eps file.

## Installation

```raw
pip install turtle-tools
```

## Example

```python
import turtle
import turtle_tools

turtle_tools.extend_turtle()

pen = turtle.Turtle()

with disable_autoupdate():
    for i in range(2):
        with pen.fill(), pen.color("blue", "green"):
            for i in range(4):
                pen.forward(100)
                pen.right(90)

        with pen.penup():
            pen.forward(150)

with pen.pensize(5):
    pen.right(90)
    pen.penup()
    pen.forward(200)
    with pen.pendown():
        pen.forward(100)
    pen.right(90)
    pen.forward(200)
    pen.pendown()
    pen.forward(200)

for i in range(2):
    with pen.poly(), pen.color("red"):
        for i in range(4):
            pen.forward(100)
            pen.right(90)

    with pen.penup():
        pen.forward(10)

save_postscript("file.eps")
turtle.done()
```

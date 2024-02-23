import turtle
from contextlib import ContextDecorator, contextmanager


class TurtleContext(ContextDecorator):
    def __repr__(self):
        classname = self.__class__.__name__
        argstr = ", ".join(
            f"{arg}={getattr(self, arg)}"
            for arg in dir(self)
            if not arg.startswith("_")
        )
        return f"{classname}({argstr})"

    def __enter__(self):
        return self


class PenContext(TurtleContext):
    def __init__(self, turtle, **pendict):
        self._turtle = turtle
        self._old_pendict = turtle.pen()
        self.pendict = pendict
        turtle.pen(**pendict)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._turtle.pen(**self._old_pendict)

    def __repr__(self):
        classname = self.__class__.__name__
        argstr = ", ".join(f"{key}={value}" for key, value in self.pendict)
        return f"{classname}({argstr})"


class PenUpContext(PenContext):
    def __init__(self, turtle):
        super().__init__(turtle, pendown=False)


class PenDownContext(PenContext):
    def __init__(self, turtle):
        super().__init__(turtle, pendown=True)


class ColorContext(PenContext):
    def __init__(self, turtle, *args):
        l = len(args)  # noqa: E741
        if l == 1:
            pcolor = fcolor = args[0]
        elif l == 2:
            pcolor, fcolor = args
        elif l == 3:
            pcolor = fcolor = args
        super().__init__(turtle, pencolor=pcolor, fillcolor=fcolor)


class PenColorContext(PenContext):
    def __init__(self, turtle, *args):
        color = turtle._colorstr(args)
        super().__init__(turtle, pencolor=color)


class FillColorContext(PenContext):
    def __init__(self, turtle, *args):
        color = turtle._colorstr(args)
        super().__init__(turtle, fillcolor=color)


class PenSizeContext(PenContext):
    def __init__(self, turtle, width):
        super().__init__(turtle, pensize=width)


class SpeedContext(PenContext):
    def __init__(self, turtle, speed):
        speeds = {
            "fastest": 0,
            "fast": 10,
            "normal": 6,
            "slow": 3,
            "slowest": 1,
        }
        if speed in speeds:
            speed = speeds[speed]
        elif 0.5 < speed < 10.5:
            speed = int(round(speed))
        else:
            speed = 0

        super().__init__(turtle, speed=speed)


class ExtendedTurtle(turtle.Turtle):
    zorder = 0

    def penup(self):
        return PenUpContext(self)

    def pendown(self):
        return PenDownContext(self)

    def color(self, *args):
        if not args:
            return super().color()
        return ColorContext(self, *args)

    def pencolor(self, *args):
        if not args:
            return super().pencolor()
        return PenColorContext(self, *args)

    def fillcolor(self, *args):
        if not args:
            return super().fillcolor()
        return FillColorContext(self, *args)

    def speed(self, *args):
        if not args:
            return super().speed()
        return SpeedContext(self, *args)

    @contextmanager
    def fill(self):
        self.begin_fill()
        yield
        self.end_fill()

    @contextmanager
    def poly(self):
        self.begin_poly()
        yield
        self.end_poly()

    def pensize(self, width=None):
        if width is None:
            return super().pensize()
        return PenSizeContext(self, width)


class disable_autoupdate(TurtleContext):
    def __init__(self):
        self._initial_tracer = turtle.tracer()
        turtle.tracer(False)

    def __exit__(self, exc_type, exc_value, exc_tb):
        turtle.tracer(self._initial_tracer)
        # turtle.update() is called by turtle.tracer, so the canvas will
        # update once the context is exited


class enable_autoupdate(TurtleContext):
    def __init__(self):
        self._initial_tracer = turtle.tracer()
        turtle.tracer(True)

    def __exit__(self, exc_type, exc_value, exc_tb):
        turtle.tracer(self._initial_tracer)


def save_postscript(filename):
    turtle.getscreen().getcanvas().postscript(file=filename)


def extend_turtle():
    turtle.Turtle = ExtendedTurtle
    turtle.disable_autoupdate = disable_autoupdate
    turtle.enable_autoupdate = enable_autoupdate
    turtle.save_postscript = save_postscript


if __name__ == "__main__":
    pen = ExtendedTurtle()
    pen.speed()

    with disable_autoupdate():
        for i in range(2):
            with pen.fill(), pen.color("blue", "green"):
                for i in range(4):
                    pen.forward(100)
                    pen.right(90)

            with pen.penup():
                pen.forward(150)

        turtle.update()

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

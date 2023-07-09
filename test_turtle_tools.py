import turtle

import pytest

import turtle_tools


class BaseTestTurtleContext:
    attribute: str = ""
    context: type = object()

    @pytest.fixture
    def turtle(self):
        return turtle.Turtle()

    def get_attribute_value(self, turtle):
        return getattr(turtle, self.attribute)()

    def test_context_resets(self, turtle, changed_attr_val, args):
        initial_attribute_value = self.get_attribute_value(turtle)
        with self.context(turtle, *args) as _ctx:  # as _ctx for debugging
            pass
        assert self.get_attribute_value(turtle) == initial_attribute_value

    def test_context_changes_correctly(self, turtle, changed_attr_val, args):
        with self.context(turtle, *args) as _ctx:  # as _ctx for debugging
            assert self.get_attribute_value(turtle) == changed_attr_val

    def test_use_as_function(self, turtle, changed_attr_val, args):
        _ctx = self.context(turtle, *args)  # store in _ctx for debugging
        assert self.get_attribute_value(turtle) == changed_attr_val


@pytest.mark.parametrize(
    "changed_attr_val, args",
    (
        (("red", "blue"), ("red", "blue")),
        (((0, 1, 0), (0, 1, 1)), ((0, 1, 0), (0, 1, 1))),
    ),
)
class TestColorContext(BaseTestTurtleContext):
    attribute = "color"
    context = turtle_tools.ColorContext


@pytest.mark.parametrize(
    "changed_attr_val, args", (("red", ("red",)), ((0, 1, 0), ((0, 1, 0),)))
)
class TestPenColorContext(BaseTestTurtleContext):
    attribute = "pencolor"
    context = turtle_tools.PenColorContext


@pytest.mark.parametrize(
    "changed_attr_val, args", (("red", ("red",)), ((0, 1, 0), ((0, 1, 0),)))
)
class TestFillColorContext(BaseTestTurtleContext):
    attribute = "fillcolor"
    context = turtle_tools.FillColorContext


@pytest.mark.parametrize("changed_attr_val, args", ((2, (2,)), (10, (10,))))
class TestPenSizeContext(BaseTestTurtleContext):
    attribute = "pensize"
    context = turtle_tools.PenSizeContext


@pytest.mark.parametrize(
    "changed_attr_val, args", ((5, (5,)), (10, ("fast",)))
)
class TestSpeedContext(BaseTestTurtleContext):
    attribute = "speed"
    context = turtle_tools.SpeedContext


class TestDisableAutoupdate:
    @pytest.fixture
    def turtle(self):
        yield turtle
        turtle.tracer(1)

    @pytest.mark.parametrize("initial_tracer", [0, 1, 2, 5])
    def test_context_resets(self, turtle, initial_tracer):
        turtle.tracer(initial_tracer)
        with turtle_tools.disable_autoupdate() as _ctx:
            pass
        assert turtle.tracer() == initial_tracer

    def test_context_changes_correctly(self, turtle):
        with turtle_tools.disable_autoupdate() as _ctx:
            assert turtle.tracer() == 0

    def test_use_as_function(self, turtle):
        _ctx = turtle_tools.disable_autoupdate()
        assert turtle.tracer() == 0


class TestEnableAutoupdate:
    @pytest.fixture
    def turtle(self):
        turtle.tracer(0)
        yield turtle
        turtle.tracer(1)

    @pytest.mark.parametrize("initial_tracer", [0, 1, 2, 5])
    def test_context_resets(self, turtle, initial_tracer):
        turtle.tracer(initial_tracer)
        with turtle_tools.enable_autoupdate() as _ctx:
            pass
        assert turtle.tracer() == initial_tracer

    def test_context_changes_correctly(self, turtle):
        with turtle_tools.enable_autoupdate() as _ctx:
            assert turtle.tracer() == 1

    def test_use_as_function(self, turtle):
        _ctx = turtle_tools.enable_autoupdate()
        assert turtle.tracer() == 1


def test_save_postscript(tmp_path):
    import turtle

    turtle.forward(10)
    turtle_tools.save_postscript(tmp_path / "file.eps")
    # Check only if file exists since file content is OS dependent
    assert (tmp_path / "file.eps").is_file()


@pytest.fixture
def cleanup_turtle():
    OldTurtle = turtle.Turtle
    yield
    turtle.Turtle = OldTurtle


def test_extend_turtle(cleanup_turtle):
    turtle_tools.extend_turtle()
    assert turtle.Turtle is turtle_tools.ExtendedTurtle


def test_extended_turtle():
    t = turtle_tools.ExtendedTurtle()
    with (
        t.penup() as penup,
        t.pendown() as pendown,
        t.color("red", "green") as color,
        t.pencolor("blue") as pencolor,
        t.fillcolor("black") as fillcolor,
        t.pensize(2) as pensize,
        t.speed(5) as speed,
        t.fill() as _fill,  # fill is created with contextlib.contextmanager
        t.poly() as _poly,  # poly is created with contextlib.contextmanager
    ):
        assert type(penup) == turtle_tools.PenUpContext
        assert type(pendown) == turtle_tools.PenDownContext
        assert type(color) == turtle_tools.ColorContext
        assert type(pencolor) == turtle_tools.PenColorContext
        assert type(fillcolor) == turtle_tools.FillColorContext
        assert type(pensize) == turtle_tools.PenSizeContext
        assert type(speed) == turtle_tools.SpeedContext

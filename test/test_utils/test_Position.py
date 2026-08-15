import pytest

from utils.Position import Position


@pytest.mark.parametrize(
    'x, y',
    [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, 1),
        (0, 0),
        (-1, -1),
    ]
)
def test_position(x, y):
    pos = Position(x, y)
    assert pos.x == x and pos.y == y

def test_position2():
    pos = Position(5, 2)
    assert pos.x == 5 and pos.y == 2
    pos.x = 10
    pos.y = -1
    assert pos.x == 10 and pos.y == -1
    pos.x = 0
    pos.y = 0
    assert pos.x == 0 and pos.y == 0
    pos.x = -5
    pos.y = -1
    assert pos.x == -5 and pos.y == -1

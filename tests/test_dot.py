import pytest
from pygame.math import Vector2
import random
from statistics import mean
from things import Dot

@pytest.fixture()
def initialize_dot():
    yield Dot()


def test_init(initialize_dot):
    dot = initialize_dot
    assert dot.mass == 0
    assert dot.position == Vector2(0, 0)


def test_randomize(initialize_dot):
    dot = initialize_dot
    dot.randomize()
    assert dot
    assert 0 <= dot.mass <= 1
    assert -1 <= dot.x <= 1
    assert -1 <= dot.y <= 1


@pytest.mark.parametrize("offset", [[1, 0],[0, 1]])
def test_move_by(initialize_dot, offset):
    dot = initialize_dot
    assert dot.position == Vector2(0, 0)

    offset = Vector2(offset)
    dot.move_by(offset)

    assert dot.position == offset


def test_move_to(initialize_dot):
    dot = initialize_dot
    assert dot.position == Vector2(0, 0)

    new_pos = Vector2(random.random(), random.random())
    dot.move_to(new_pos)
    assert dot.position == Vector2(new_pos)


def test_change_mass(initialize_dot):
    dot = initialize_dot
    assert dot.mass == 0
    dot.change_mass_by(1)
    assert dot.mass == 1

    dot.change_mass_to(2)
    assert dot.mass == 2


def test_string(initialize_dot):
    dot = initialize_dot
    assert str(dot) == f"Mass: {dot.mass:0.2f}\nPosition: [{dot.x:0.2f},{dot.y:0.2f}]"
    dot.change_mass_by(1)
    dot.move_to([1,2])
    assert str(dot) == f"Mass: {dot.mass:0.2f}\nPosition: [{dot.x:0.2f},{dot.y:0.2f}]"


def test_random_walk(initialize_dot):
    dot = initialize_dot
    max_distance = 1
    distances = []
    for i in range(10000):
        offset = dot.random_walk(max_distance=max_distance)
        assert offset.magnitude() <= max_distance
        distances.append(offset.magnitude())
    print(mean(distances))
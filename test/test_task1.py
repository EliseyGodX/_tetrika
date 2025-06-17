import pytest

from task1.solution import strict


@strict
def func(a: int, b: int, c=None) -> int:
    return a + b


def test_correct_types():
    assert func(1, 2) == 3


def test_wrong_type():
    with pytest.raises(TypeError):
        func('1', 2)

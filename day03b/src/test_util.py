from .util import find_sum


def test_find_sum():
    answer = find_sum('input.test.txt')
    assert answer == 467835

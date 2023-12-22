from .utils import find_answer, find_differences, find_next


def test_find_differences_basic():
    seq = [0, 3, 6, 9, 12, 15]
    expected = [3, 3, 3, 3, 3]
    actual = find_differences(seq)
    assert expected == actual


def test_find_next_basic():
    seq = [0, 3, 6, 9, 12, 15]
    expected = 18
    actual = find_next(seq)
    assert expected == actual


def test_find_next_med():
    seq = [1, 3, 6, 10, 15, 21]
    expected = 28
    actual = find_next(seq)
    assert expected == actual


def test_find_next_hard():
    seq = [10, 13, 16, 21, 30, 45]
    expected = 68
    actual = find_next(seq)
    assert expected == actual


def test_find_answer():
    expected = 114
    actual = find_answer("input.test.txt")
    assert expected == actual

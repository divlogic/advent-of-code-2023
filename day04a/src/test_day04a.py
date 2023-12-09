from .util import find_sum, check_points


def test_line_1():
    line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n"
    assert 8 == check_points(line)


def test_line_2():
    line = "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n"
    assert 2 == check_points(line)


def test_line_3():
    line = "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n"
    assert 2 == check_points(line)


def test_line_4():
    line = "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n"
    assert 1 == check_points(line)


def test_line_5():
    line = "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n"
    assert 0 == check_points(line)


def test_line_6():
    line = "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n"
    assert 0 == check_points(line)


def test_find_sum():
    answer = find_sum('input.test.txt')
    assert answer == 13

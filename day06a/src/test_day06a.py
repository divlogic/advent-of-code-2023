import re
from pathlib import Path

from .utils import count_viable, find_answer, generate_data


def test_generate_data():
    store = {}
    time = 7

    generate_data(store, time)

    expected = {
        0: 0,
        1: 6,
        2: 10,
        3: 12,
        4: 12,
        5: 10,
        6: 6,
    }
    assert store == expected


def test_find_count_short():
    time = 7
    record = 9

    store = {}

    actual = count_viable(store, time, record)

    expected = 4

    assert actual == expected


def test_find_count_med():
    time = 15
    record = 40

    store = {}

    actual = count_viable(store, time, record)

    expected = 8

    assert actual == expected


def test_find_count_longest():
    time = 30
    record = 200

    store = {}

    actual = count_viable(store, time, record)

    expected = 9

    assert actual == expected


def test_find_answer():
    filename = "input.test.txt"
    expected = 288
    actual = find_answer(filename)

    assert expected == actual

import re
from pathlib import Path
from typing import Dict


def generate_data(store: Dict, time: int):
    """Mutates the store to fill it with possible times"""
    for i in range(0, time):
        speed = i
        time_left = time - i
        distance_traveled = int(speed * time_left)
        store[i] = distance_traveled


def count_viable(store, time, record):
    generate_data(store, time)
    winning_runs = list(filter(lambda item: item[1] > record, store.items()))
    viable_count = len(winning_runs)

    return viable_count


def find_answer(filename):
    lines = None

    with open(Path(__file__).parents[1] / (filename)) as file:
        lines = file.readlines()

    time = int("".join(re.findall(r"(\d+)", lines[0])))
    record = int("".join(re.findall(r"(\d+)", lines[1])))

    store = {}
    answer = count_viable(store, time, record)
    return answer

import math
import re
from pathlib import Path
from typing import Dict

"""
Idea 1

1. For each value in the series of times that it's possible
    to hold the button down:
    2. Calculate what distance it can travel in its remaining duration
    3. Assign that value to some kind of dictionary,
        something like {(time_pressed): (distance traveled)}
    
    For each time/record:
        Count all of the above items that have a higher distance than the record
    
    Multiply this group of numbers

    
"""


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

    times = re.findall(r"(\d+)", lines[0])
    records = re.findall(r"(\d+)", lines[1])
    input_data = dict(
        zip([int(item) for item in times], [int(item) for item in records])
    )

    viable_counts = []
    store = {}
    for time, record in input_data.items():
        viable_counts.append(count_viable(store, time, record))
    answer = int(math.prod(viable_counts))
    print(answer)
    return answer

import math
from pathlib import Path
from typing import List


def find_differences(seq: List[int]) -> List[int]:
    differences = [
        seq[index + 1] - seq[index]
        for index in range(0, len(seq))
        if index < len(seq) - 1
    ]
    return differences


def find_next(seq: List[int]) -> int:
    limit = 100
    count = 0
    sequences = [seq]
    while count < limit:
        differences = find_differences(sequences[-1])
        sequences.append(differences)
        if sequences[-1].count(0) == len(sequences[-1]):
            break
        count += 1
    sequences[-1].append(0)

    count = 0
    while count < limit and count < len(sequences) - 1:
        negative_index = -1 * (count + 2)
        below = sequences[negative_index + 1][0]

        left = sequences[negative_index][0]
        next_number = left - below
        sequences[negative_index].insert(0, next_number)
        count += 1

    return seq[0]


def find_answer(filename) -> int:
    with open(Path(__file__).parents[1] / (filename)) as file:
        lines = file.readlines()

    next_numbers = []

    for line in lines:
        seq = [int(character) for character in line.split(" ")]
        next = find_next(seq)
        next_numbers.append(next)

    answer = int(math.fsum(next_numbers))
    return answer

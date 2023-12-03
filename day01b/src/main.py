import re
import os
from pathlib import Path

numbers_dict = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

written_numbers_pattern = "|".join(numbers_dict.keys())
numbers_pattern = "(?=(\d|" + written_numbers_pattern + "))"

numbers_list = []

with open(Path(__file__).parents[1] / ("input.txt")) as input:
    for line in input:
        numbers = re.findall(numbers_pattern, line)
        first_digit = str(
            numbers[0] if numbers[0] not in numbers_dict else numbers_dict[numbers[0]])
        second_digit = str(
            numbers[-1] if numbers[-1] not in numbers_dict else numbers_dict[numbers[-1]])
        correct_number = int(first_digit + second_digit)
        numbers_list.append(correct_number)

answer = sum(numbers_list)

print(answer)

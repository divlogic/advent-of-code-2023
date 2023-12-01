import re
import os
from pathlib import Path


numbers_list = []

with open(Path(__file__).parents[1] / ("input.txt")) as input:
    for line in input:
        numbers = re.findall("\d", line)
        correct_number = int(numbers[0] + numbers[-1])
        numbers_list.append(correct_number)

answer = sum(numbers_list)
print(answer)

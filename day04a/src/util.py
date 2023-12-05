from pathlib import Path
import math
import re
import pprint


def check_points(line):
    card = line.split('|')
    winning_numbers = re.findall(
        r'(?:^Card \d+:\s)?(?:(?P<winning_number>\d+)\s)', card[0])

    winning_numbers_pattern = '|'.join(winning_numbers)
    matching_pattern = fr"""
            (?=(?:\s)
            ({winning_numbers_pattern})
            (?:\s|$))
            
        """

    matching_numbers = re.findall(
        matching_pattern, card[1], re.VERBOSE)
    matches = len(matching_numbers)
    points = 0
    for i in range(1, matches + 1):
        if i == 1:
            points += 1
        else:
            points *= 2
    return points


def find_sum(file):
    numbers_to_sum = []
    with open(Path(__file__).parents[1] / (file)) as input:
        for index, line in enumerate(input):
            points = check_points(line)
            numbers_to_sum.append(points)

    answer = int(math.fsum(numbers_to_sum))
    return answer

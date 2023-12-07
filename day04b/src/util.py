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
    return matches


def find_sum(file):
    totals = {}
    with open(Path(__file__).parents[1] / (file)) as input:
        for index, line in enumerate(input):
            totals[index] = totals.get(index, 0) + 1
            matches = check_points(line)
            # For as many copies of a card, with a minimum of 1
            for j in range(0, totals[index]):
                # Distribute the number of matches to the following cards
                for i in range(index + 1, index + matches + 1):
                    totals[i] = totals.get(i, 0) + 1

    answer = int(math.fsum(totals.values()))
    return answer

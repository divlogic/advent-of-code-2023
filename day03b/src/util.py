
from pathlib import Path
import math
import re


def find_sum(file):
    numbers_to_sum = []
    parsed_numbers = {}
    gears = {}
    with open(Path(__file__).parents[1] / (file)) as input:
        for line_index, line in enumerate(input):
            parsed_numbers[line_index] = {}
            gears[line_index] = {}
            line_items = re.finditer(
                r'(?P<number>\d+)|(?P<gear>\*)', line)
            for item in line_items:
                number = item.group('number')
                gear = item.group('gear')
                if number is not None:
                    for position in range(*item.span()):
                        parsed_numbers[line_index][position] = (
                            item.span(), int(number))
                if gear is not None:
                    for position in range(*item.span()):
                        gears[line_index][position] = gear
    for line_number, line in gears.items():
        previous_line = line_number - 1
        next_line = line_number + 1
        for position, gear in line.items():
            left = position - 1
            right = position + 1
            adjacent_numbers = {}
            # Need to capture all adjacent but not duplicate it
            # Left and right

            current_line_numbers = parsed_numbers[line_number]
            if (left) in parsed_numbers[line_number]:
                adjacent_numbers[(line_number, current_line_numbers[left]
                                 [0])] = current_line_numbers[left][1]
            if (right) in parsed_numbers[line_number]:
                adjacent_numbers[(line_number, current_line_numbers[right]
                                 [0])] = current_line_numbers[right][1]

            # Below
            if gears.get(next_line) is not None:
                next_line_numbers = parsed_numbers[next_line]
                if (left) in parsed_numbers.get(next_line):
                    adjacent_numbers[(next_line, next_line_numbers[left]
                                     [0])] = next_line_numbers[left][1]
                if (position) in parsed_numbers.get(next_line):
                    adjacent_numbers[(next_line, next_line_numbers[position]
                                     [0])] = next_line_numbers[position][1]
                if (right) in parsed_numbers.get(next_line):
                    adjacent_numbers[(next_line, next_line_numbers[right]
                                     [0])] = next_line_numbers[right][1]
            # Above
            if gears.get(previous_line) is not None:
                previous_line_numbers = parsed_numbers[previous_line]
                if (left) in parsed_numbers.get(previous_line):
                    adjacent_numbers[(previous_line, previous_line_numbers[left]
                                     [0])] = previous_line_numbers[left][1]
                if (position) in parsed_numbers.get(previous_line):
                    adjacent_numbers[(previous_line, previous_line_numbers[position]
                                     [0])] = previous_line_numbers[position][1]
                if (right) in parsed_numbers.get(previous_line):
                    adjacent_numbers[(previous_line, previous_line_numbers[right]
                                     [0])] = previous_line_numbers[right][1]
            if len(adjacent_numbers) == 2:
                numbers_to_sum.append(math.prod(adjacent_numbers.values()))

    answer = int(math.fsum(numbers_to_sum))
    return answer

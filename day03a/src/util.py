
from pathlib import Path
import math
import re


def find_sum(file):
    numbers_to_sum = []
    parsed_numbers = {}
    parsed_symbols = {}
    with open(Path(__file__).parents[1] / (file)) as input:
        for line_index, line in enumerate(input):
            parsed_numbers[line_index] = {}
            parsed_symbols[line_index] = {}
            line_items = re.finditer(
                '(?P<number>\d+)|(?P<symbol>[^0-9.\r\n])', line)
            for item in line_items:
                number = item.group('number')
                symbol = item.group('symbol')
                if number is not None:
                    parsed_numbers[line_index][range(
                        *item.span())] = int(number)
                if symbol is not None:
                    for position in range(*item.span()):
                        parsed_symbols[line_index][position] = symbol
    for line_number, line in parsed_numbers.items():
        previous_line = line_number - 1
        next_line = line_number + 1
        for span, number in line.items():
            for position in span:
                # Left and right
                if (position - 1) in parsed_symbols[line_number]:
                    numbers_to_sum.append(number)
                    break
                if (position + 1) in parsed_symbols[line_number]:
                    numbers_to_sum.append(number)
                    break

                # Below
                if parsed_symbols.get(next_line) is not None:
                    if (position - 1) in parsed_symbols.get(line_number+1):
                        numbers_to_sum.append(number)
                        break
                    if (position) in parsed_symbols.get(next_line):
                        numbers_to_sum.append(number)
                        break
                    if (position + 1) in parsed_symbols.get(next_line):
                        numbers_to_sum.append(number)
                        break
                # Above
                if parsed_symbols.get(previous_line) is not None:
                    if (position - 1) in parsed_symbols.get(previous_line):
                        numbers_to_sum.append(number)
                        break
                    if (position) in parsed_symbols.get(previous_line):
                        numbers_to_sum.append(number)
                        break
                    if (position + 1) in parsed_symbols.get(previous_line):
                        numbers_to_sum.append(number)
                        break
    answer = int(math.fsum(numbers_to_sum))
    return answer

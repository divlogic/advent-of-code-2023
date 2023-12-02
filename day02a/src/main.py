from pathlib import Path
import math
import re

colors_limits = {'red': 12, 'green': 13, 'blue': 14}


possible_games = []

with open(Path(__file__).parents[1] / ("input.txt")) as input:
    for line in input:
        possible = True
        id = re.search('Game (\d+)', line).group(1)
        color_counts = {'red': 0, 'green': 0, 'blue': 0}
        for color in color_counts.keys():
            counts = [int(count) for count in re.findall(
                f'(\d+) {color}', line)]
            for count in counts:
                if count > colors_limits[color]:
                    possible = False
        if possible is True:
            possible_games.append(int(id))

print(int(math.fsum(possible_games)))

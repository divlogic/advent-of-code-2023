from pathlib import Path
import math
import re
import pprint

seed_pattern = r'(?:seeds:\s)?(\d+)'

range_pattern = r'(\d+)'


class SeedMapper:
    def __init__(self, seeds: list[str]) -> None:
        self.seeds = [int(seed) for seed in seeds]
        self.current_map = {}
        for seed in self.seeds:
            self.current_map[seed] = None

    def map_current_to_next(self, line: list[str] | None = None):
        if line is not None:
            data = re.findall(range_pattern, line)
            destination_range_start = int(data[0])
            source_range_start = int(data[1])
            range_length = int(data[2])
            for item, value in self.current_map.items():
                if value is None:
                    if item >= source_range_start and item <= source_range_start + range_length:
                        self.current_map[item] = int(destination_range_start) + \
                            int(item) - int(source_range_start)
        else:
            for item, value in self.current_map.items():
                if value is None:
                    self.current_map[item] = int(item)

    def orient_map(self):
        new_map = {}
        for value in self.current_map.values():
            new_map[value] = None
        self.current_map = new_map


def find_answer(file):
    locations = []
    with open(Path(__file__).parents[1] / (file)) as input:
        seeds = None
        mapper = None
        for index, line in enumerate(input):
            if index == 0:
                seeds = re.findall(seed_pattern, line)
                mapper = SeedMapper(seeds)
            elif index < 3:
                # Ignore first blank line
                continue
            elif re.match(r'\d', line) is not None:
                mapper.map_current_to_next(line)
            elif len(line) == 1:
                mapper.map_current_to_next()
            elif re.match(r'\w', line) is not None:
                # We don't actually have to programmatically know which map is which
                # because it's ordered
                mapper.orient_map()
        mapper.map_current_to_next()

    answer = min(mapper.current_map.values())
    return answer

from pathlib import Path
import re
from .converter import map_range_group, ParsedRangeMap

seed_pattern = r'(?:seeds:\s)?(\d+)'

range_pattern = r'(\d+)'
empty_line_pattern = r'(?P<empty_line>^$)'


class RangeParser:
    def __init__(self, filename) -> None:
        lines = None
        with open(Path(__file__).parents[1] / (filename)) as input:
            lines = input.readlines()
        seed_data = re.findall(seed_pattern, lines[0])
        seeds = sorted([ParsedRangeMap(source_range=(int(seed[0]), int(seed[0]) + int(seed[1])))
                        for seed in zip(seed_data[::2], seed_data[1::2])], key=lambda item: item.source_range)

        self.seed_ranges = seeds

        self.range_maps = []
        new_map = True
        for line in lines[2:]:
            empty = re.search(empty_line_pattern, line)
            if new_map:
                if len(self.range_maps) > 0:
                    self.range_maps[-1].sort(
                        key=lambda item: item['destination_range_start'])
                self.range_maps.append([])
                new_map = False
                continue
            if empty is not None:
                new_map = True
            elif re.search('[a-zA-Z]', line) is not None:
                continue
            else:
                data = re.findall(range_pattern, line)
                destination_range_start = int(data[0])
                source_range_start = int(data[1])
                range_length = int(data[2])
                self.range_maps[-1].append({})
                self.range_maps[-1][-1]['destination_range_start'] = destination_range_start
                self.range_maps[-1][-1]['source_range_start'] = source_range_start
                self.range_maps[-1][-1]['range_length'] = range_length


def find_answer(file):
    print()
    print('STARTING')
    parser = RangeParser(file)
    range_groups = parser.range_maps
    sources = parser.seed_ranges
    for index, range_group in enumerate(range_groups):
        print('Currently on group: ' + str(index))
        mapped_ranges = map_range_group(sources, range_group)

        sources = [ParsedRangeMap(
            parent=item, source_range=item.destination_range) for item in mapped_ranges]

    answer = mapped_ranges[0].destination_range[0]
    return answer

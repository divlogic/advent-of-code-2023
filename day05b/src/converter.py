from __future__ import annotations
from typing import List, Tuple, Type, Dict
from dataclasses import dataclass
from pydantic import BaseModel
import math


@dataclass
class DestinationMap:
    """source_range_start is inclusive
    source_range_start + range_length is non inclusive
    example:
    source_range_start = 98
    range_length = 2
    If you map that out, it comes out to:
    [98, 99]
    """
    destination_range_start: int
    source_range_start: int
    range_length: int


@dataclass
class ParsedRangeMap:
    parent: ParsedRangeMap | None = None
    range_map: DestinationMap | None = None
    source_range: Tuple[int, int] | None = None
    destination_range: Tuple[int, int] | None = None
    exhausted: bool = False
    split: bool | None = None


class RangeMapGroup:
    def __init__(self, name: str) -> None:
        self.container: dict[Tuple, ParsedRangeMap] = {}
        self.name = name

    def __len__(self):
        return len(self.container)

    def add(self, item: ParsedRangeMap):
        if item.source_range in self.container:
            message = f'Source range {item.source_range} already in container'
            raise (Exception(message))
        self.container[item.source_range] = item

    def remove_item(self, item: ParsedRangeMap):
        del self.container[item.source_range]

    def extend(self, group: List[ParsedRangeMap]):
        for item in group:
            if item.source_range in self.container:
                message = f'Source range {item.source_range} already in container'
                raise (Exception(message))
            self.add(item)

    def clear_exhausted(self):
        items_to_remove = []
        for key, value in self.container.items():
            if value.exhausted is True:
                items_to_remove.append(value)

        for item in items_to_remove:
            self.remove_item(item)


def source_to_dest(source: int, parsed_range: {'source_range_start': int, 'destination_range_start': int, 'range_length': int}) -> int:
    if source < parsed_range['source_range_start']:
        raise ('Invalid number')
    return parsed_range['destination_range_start'] + source - parsed_range['source_range_start']


def range_contains_number(dest_range: (int, int), num: int, start: bool):
    if start is True:
        if num >= dest_range[0] and num < dest_range[1]:
            return True
    else:
        if num > dest_range[0] and num <= dest_range[1]:
            return True

    return False


def source_range_to_tuple(parsed_range: {'source_range_start': int, 'source_range_start': int, 'range_length': int}):
    return (parsed_range['source_range_start'], parsed_range['source_range_start'] + parsed_range['range_length'])


def dest_range_to_tuple(parsed_range: {'source_range_start': int, 'destination_range_start': int, 'range_length': int}):
    return (parsed_range['destination_range_start'], parsed_range['destination_range_start'] + parsed_range['range_length'])


def try_source_to_destination(initial_parsed_range_map: ParsedRangeMap, dest: {'source_range_start': int, 'destination_range_start': int, 'range_length': int}):
    result = []
    source_tuple = source_range_to_tuple(dest)
    start_is_in = range_contains_number(
        source_tuple, initial_parsed_range_map.source_range[0], True)
    end_is_in = range_contains_number(
        source_tuple, initial_parsed_range_map.source_range[1], False)
    source = initial_parsed_range_map.source_range
    if start_is_in and end_is_in:
        mapped_range = ParsedRangeMap(
            source_range=initial_parsed_range_map.source_range,
            range_map=DestinationMap(**dest),
            destination_range=(
                source_to_dest(
                    source[0], dest
                ),
                source_to_dest(
                    source[1],
                    dest
                )
            ),
            exhausted=True,
            parent=initial_parsed_range_map,
            split=False
        )
        result.append(mapped_range)
        return result
    if start_is_in and not end_is_in:
        new_mapped_range = ParsedRangeMap(parent=initial_parsed_range_map, source_range=(
            source[0], dest['source_range_start'] + dest['range_length']),
            destination_range=(source_to_dest(source[0], dest), source_to_dest(
                dest['source_range_start'] + dest['range_length'], dest)),
            range_map=DestinationMap(**dest),
            exhausted=True,
            split=True
        )
        new_unmapped_range = ParsedRangeMap(parent=initial_parsed_range_map, source_range=(
            dest['source_range_start'] + dest['range_length'], source[1]),
            destination_range=None,
            split=True
        )

        result.append(new_mapped_range)
        result.append(new_unmapped_range)
        return result

    if end_is_in and not start_is_in:
        new_mapped_range = ParsedRangeMap(
            source_range=(dest['source_range_start'], source[1]),
            destination_range=(source_to_dest(
                dest['source_range_start'], dest),
                source_to_dest(source[1], dest)
            ),
            range_map=DestinationMap(**dest),
            parent=initial_parsed_range_map,
            exhausted=True,
            split=True
        )

        new_unmapped_range = ParsedRangeMap(
            source_range=(source[0], dest['source_range_start']),
            destination_range=None,
            parent=initial_parsed_range_map,
            split=True
        )
        result.append(new_unmapped_range)
        result.append(new_mapped_range)
        return result
    return None


def map_source_to_range_group(source: ParsedRangeMap, destinations) -> List[ParsedRangeMap] | None:
    ranges = RangeMapGroup('ranges')
    for dest in destinations:
        result_ranges = try_source_to_destination(source, dest)
        if result_ranges is not None:
            ranges.extend(result_ranges)
            return ranges
    return None


def map_range_group(init_ranges: List[ParsedRangeMap], dest_ranges: [{'source_range_start': int, 'source_range_start': int, 'range_length': int}]) -> List[ParsedRangeMap]:
    # "prod" file is less than 300 lines,
    # so there shouldn't be that much of a need to reduce size outside of not mapping specific locations
    unexhausted_ranges = RangeMapGroup('unexhausted_ranges')
    unexhausted_ranges.extend(init_ranges)
    mapped_ranges = RangeMapGroup('mapped_ranges')
    unmapped_ranges = RangeMapGroup('unmapped_ranges')

    count = 0
    while count < 20 and len(unexhausted_ranges) > 0:
        items_to_add = RangeMapGroup('items_to_add')
        for source in unexhausted_ranges.container.values():
            result_ranges = map_source_to_range_group(source, dest_ranges)

            # That means nothing was able to be mapped
            source.exhausted = True
            if result_ranges is None:
                unmapped_ranges.add(source)
            else:
                # Mutates everything it's passed
                handle_result_ranges(result_ranges, mapped_ranges,
                                     items_to_add, unmapped_ranges)

            # The source has been applied to all destination ranges
            source.exhausted = True

        unexhausted_ranges.clear_exhausted()
        unexhausted_ranges.extend(items_to_add.container.values())

        count += 1

    for item in unmapped_ranges.container.values():
        item.destination_range = item.source_range
        mapped_ranges.add(item)

    return sorted(mapped_ranges.container.values(), key=lambda item: item.destination_range)


def handle_result_ranges(result_ranges, mapped_ranges, items_to_add, unmapped_ranges):
    if result_ranges is not None:
        for item in result_ranges.container.values():
            if item.destination_range is not None:
                mapped_ranges.add(item)
                item.exhausted = True
            elif item.exhausted is False:
                items_to_add.add(item)
            elif item.exhausted is True and item.destination_range is None:
                unmapped_ranges.append(item)

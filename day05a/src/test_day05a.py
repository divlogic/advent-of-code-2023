from .util import seed_pattern, range_pattern, find_answer, SeedMapper
import re
from decimal import Decimal

# Test that the data is correctly parsed
# Tests that:
# Seed number 79 corresponds to soil number 81.
# Seed number 14 corresponds to soil number 14.
# Seed number 55 corresponds to soil number 57.
# Seed number 13 corresponds to soil number 13.


def test_parse_seeds():
    line = 'seeds: 79 14 55 13'
    seed_data = ['79', '14', '55', '13']
    assert seed_data == re.findall(seed_pattern, line)


def test_parse_ranges():
    range = '50 98 2'
    range_data = ['50', '98', '2']
    assert range_data == re.findall(range_pattern, range)


def test_map_seed_to_soil_unmapped():
    seed_data = ['10']

    mapper = SeedMapper(seed_data)
    mapper.map_current_to_next()

    assert {10: 10} == mapper.current_map


def test_map_seed_to_soil_simplest():
    seed_to_soil_map = ['seed-to-soil map:\n',
                        '50 98 2\n',
                        '52 50 48\n'
                        ]
    seed_data = ['98']

    mapper = SeedMapper(seed_data)
    mapper.map_current_to_next(seed_to_soil_map[1])

    assert {98: 50} == mapper.current_map


def test_map_seed_to_soil_simple():
    seed_to_soil_map = ['seed-to-soil map:\n',
                        '50 98 2\n',
                        '52 50 48\n'
                        ]
    seed_data = ['99']

    mapper = SeedMapper(seed_data)
    mapper.map_current_to_next(seed_to_soil_map[1])

    assert {99: 51} == mapper.current_map


def test_map_seed_to_soil_simple_2():
    seed_to_soil_map = ['seed-to-soil map:\n',
                        '50 98 2\n',
                        '52 50 48\n'
                        ]
    seed_data = ['53']

    mapper = SeedMapper(seed_data)
    mapper.map_current_to_next(seed_to_soil_map[2])

    assert {53: 55} == mapper.current_map


def test_map_seed_to_soil_normal():
    seed_to_soil_map = ['seed-to-soil map:\n',
                        '50 98 2\n',
                        '52 50 48\n'
                        ]
    seed_data = ['79', '14', '55', '13']

    mapper = SeedMapper(seed_data)
    mapper.map_current_to_next(seed_to_soil_map[1])
    mapper.map_current_to_next(seed_to_soil_map[2])
    mapper.map_current_to_next()

    assert {79: 81, 14: 14, 55: 57, 13: 13} == mapper.current_map


def test_mapper_update_map():
    seed_to_soil_map = ['seed-to-soil map:\n',
                        '50 98 2\n',
                        '52 50 48\n'
                        ]
    seed_data = ['79', '14', '55', '13']

    mapper = SeedMapper(seed_data)
    mapper.map_current_to_next(seed_to_soil_map[1])
    mapper.map_current_to_next(seed_to_soil_map[2])
    mapper.map_current_to_next()

    mapper.orient_map()

    assert {81: None, 14: None, 57: None, 13: None} == mapper.current_map


def test_find_answer():
    answer = find_answer('input.test.txt')
    assert answer == 35

from .util import seed_pattern, empty_line_pattern, range_pattern, find_answer, RangeParser
from .converter import source_to_dest, range_contains_number, try_source_to_destination, dest_range_to_tuple, map_range_group, ParsedRangeMap, DestinationMap, map_source_to_range_group, RangeMapGroup
import re
import pprint


def test_parse_seeds():
    line = 'seeds: 79 14 55 13'
    seed_data = ['79', '14', '55', '13']
    assert seed_data == re.findall(seed_pattern, line)


def test_parse_ranges():
    range = '50 98 2'
    range_data = ['50', '98', '2']
    assert range_data == re.findall(range_pattern, range)


def test_empty_line_pattern():
    good_line = "\n"
    bad_line = "This is a test, should not pass\n"

    result_should_pass = re.search(empty_line_pattern, good_line)[
        0]
    result_should_be_none = re.search(
        empty_line_pattern, bad_line)

    assert result_should_pass == ''
    assert result_should_be_none is None


def test_parse_file():
    filename = 'input.test.txt'
    parser = RangeParser(filename)

    # This is asserting correctness and sorting
    parsed_seed_1 = ParsedRangeMap(source_range=(55, 68))
    parsed_seed_2 = ParsedRangeMap(source_range=(79, 93))
    assert [parsed_seed_1, parsed_seed_2] == parser.seed_ranges

    assert [
        {
            'source_range_start': 98,
            'destination_range_start': 50,
            'range_length': 2
        },
        {
            'source_range_start': 50,
            'destination_range_start': 52,
            'range_length': 48
        }
    ] == parser.range_maps[0]

    assert 7 == len(parser.range_maps)


def test_convert_source_to_dest():
    source_number = 55
    parsed_range = {'destination_range_start': 52,
                    'source_range_start': 50, 'range_length': 48}

    expected = 57
    actual = source_to_dest(source_number, parsed_range)
    assert expected == actual


def test_range_contains_number():
    source_number = 55
    dest_range = (50, 98)
    expected = True
    actual = range_contains_number(dest_range, source_number, True)
    assert expected == actual


def test_range_contains_number_start_in():
    source_number = 50
    dest_range = (50, 98)
    expected = True
    actual = range_contains_number(dest_range, source_number, True)
    assert expected == actual


def test_range_contains_number_end_not_in():
    source_number = 99
    dest_range = (50, 98)
    expected = False
    actual = range_contains_number(dest_range, source_number, False)
    assert expected == actual


def test_parsed_range_to_tuple():
    parsed_range = {'destination_range_start': 52,
                    'source_range_start': 50, 'range_length': 48}
    expected = (52, 100)
    actual = dest_range_to_tuple(parsed_range)
    assert expected == actual


def test_map_ranges_easy():
    parsed_range = {'destination_range_start': 52,
                    'source_range_start': 50, 'range_length': 48}

    parent_range = ParsedRangeMap(source_range=(55, 68))
    expected_range = ParsedRangeMap(
        parent=parent_range,
        source_range=(55, 68),
        destination_range=(57, 70),
        range_map=DestinationMap(**parsed_range),
        split=False,
        exhausted=True
    )
    expected = [expected_range]
    actual = try_source_to_destination(parent_range, parsed_range)

    assert expected == actual


def test_map_ranges_start_is_out():
    parsed_range = {'destination_range_start': 52,
                    'source_range_start': 50, 'range_length': 48}

    parent_range = ParsedRangeMap(
        source_range=(45, 68)
    )
    pprint.pprint(parent_range)
    unmapped_range = ParsedRangeMap(
        source_range=(45, 50),
        destination_range=None,
        parent=parent_range,
        split=True
    )
    mapped_range = ParsedRangeMap(
        source_range=(50, 68),
        destination_range=(52, 70),
        parent=parent_range,
        split=True,
        exhausted=True,
        range_map=DestinationMap(**parsed_range)
    )
    expected = [unmapped_range, mapped_range]

    actual = try_source_to_destination(parent_range, parsed_range)

    assert len(expected) == len(actual)
    assert [item.destination_range for item in expected] == [
        item.destination_range for item in actual]
    # This needs some tweaking because I'm not property assigning the parent property
    assert expected == actual


def test_map_ranges_end_is_out():
    parsed_range = {'destination_range_start': 52,
                    'source_range_start': 50, 'range_length': 48}

    parent_range = ParsedRangeMap(source_range=(50, 100))
    mapped_range = ParsedRangeMap(
        parent=parent_range,
        source_range=(50, 98),
        destination_range=(52, 100),
        range_map=DestinationMap(**parsed_range),
        split=True,
        exhausted=True
    )
    unmapped_range = ParsedRangeMap(
        parent=parent_range, source_range=(98, 100), destination_range=None, split=True)

    expected = [mapped_range, unmapped_range]

    actual = try_source_to_destination(parent_range, parsed_range)

    assert expected == actual


def test_map_current_range_group():
    range_map_1 = {
        'destination_range_start': 50,
        'source_range_start': 98,
        'range_length': 2
    }
    range_map_2 = {
        'destination_range_start': 52,
        'source_range_start': 50,
        'range_length': 48
    }
    parent_range_1 = ParsedRangeMap(source_range=(55, 68))
    parent_range_2 = ParsedRangeMap(source_range=(79, 93))

    mapped_range_1 = ParsedRangeMap(
        parent=parent_range_1,
        source_range=(55, 68),
        destination_range=(57, 70),
        range_map=DestinationMap(**range_map_2),
        split=False,
        exhausted=True
    )

    mapped_range_2 = ParsedRangeMap(
        parent=parent_range_2,
        source_range=(79, 93),
        destination_range=(81, 95),
        range_map=DestinationMap(**range_map_2),
        split=False,
        exhausted=True
    )
    expected = [mapped_range_1, mapped_range_2]
    actual = map_range_group(
        [parent_range_1, parent_range_2],
        [range_map_1, range_map_2]
    )
    assert expected == actual


def test_map_current_range_group_no_ranges():
    parent_range_1 = ParsedRangeMap(source_range=(57, 70))
    parent_range_2 = ParsedRangeMap(source_range=(81, 95))

    expected_range_1 = ParsedRangeMap(
        source_range=(57, 70),
        destination_range=(57, 70),
        exhausted=True
    )

    expected_range_2 = ParsedRangeMap(
        source_range=(81, 95),
        destination_range=(81, 95),
        exhausted=True
    )
    expected = [
        expected_range_1,
        expected_range_2
    ]

    actual = map_range_group(
        [parent_range_1, parent_range_2],
        [
            {'destination_range_start': 0,
                'source_range_start': 39, 'range_length': 15},
            {'destination_range_start': 15,
             'source_range_start': 0, 'range_length': 37},
            {'destination_range_start': 52,
                'source_range_start': 37, 'range_length': 2}
        ]
    )
    assert actual == expected


def test_find_answer():
    answer = find_answer('input.test.txt')
    # I put in received 0 as an answer, but the site did not accept it.
    # for some reason there are destination ranges with the tuple (0, 0) in the final mapped ranges
    # That shouldn't happen
    # I put in 120063312 as an answer and that's too high.
    assert answer == 46


def test_map_source_to_range_group():
    source = ParsedRangeMap(source_range=(74, 88))
    dest_ranges = [
        {'destination_range_start': 45, 'source_range_start': 77, 'range_length': 23},
        {'destination_range_start': 68, 'source_range_start': 64, 'range_length': 13},
        {'destination_range_start': 81, 'source_range_start': 45, 'range_length': 19}]
    actual = map_source_to_range_group(source, dest_ranges)
    # Is the issue that I don't have the tuples as being inclusive of the end value?
    mapped_range_1 = ParsedRangeMap(
        parent=source,
        source_range=(77, 88),
        destination_range=(45, 56),
        range_map=DestinationMap(**dest_ranges[0]),
        exhausted=True,
        split=True
    )

    # There shouldn't be a (77, 77) to (45, 45) mapping
    unmapped_range_1 = ParsedRangeMap(
        parent=source,
        source_range=(74, 77),
        destination_range=None,
        range_map=None,
        exhausted=False,
        split=True
    )
    expected = RangeMapGroup('expected')
    expected.add(mapped_range_1)
    expected.add(unmapped_range_1)
    assert expected.container == actual.container


def test_map_source_to_range_group_followup():
    source = ParsedRangeMap(source_range=(74, 77))
    dest_ranges = [
        {'destination_range_start': 45, 'source_range_start': 77, 'range_length': 23},
        {'destination_range_start': 68, 'source_range_start': 64, 'range_length': 13},
        {'destination_range_start': 81, 'source_range_start': 45, 'range_length': 19}]
    actual = map_source_to_range_group(source, dest_ranges)
    # Is the issue that I don't have the tuples as being inclusive of the end value?
    mapped_range_1 = ParsedRangeMap(
        parent=source,
        source_range=(74, 77),
        destination_range=(78, 81),
        range_map=DestinationMap(**dest_ranges[1]),
        exhausted=True,
        split=False
    )
    expected = RangeMapGroup('expected')
    expected.add(mapped_range_1)
    assert expected.container == actual.container

from .utils import Hand, find_answer, get_ranks, get_winnings


def test_hand_strength_five():
    actual = Hand("AAAAA").strength
    expected = 7

    assert actual == expected


def test_hand_strength_four():
    actual = Hand("AA8AA").strength
    expected = 6

    assert actual == expected


def test_hand_strength_full_house():
    actual = Hand("23332").strength
    expected = 5

    assert actual == expected


def test_hand_strength_three_of_a_kind():
    actual = Hand("TTT98").strength
    expected = 4

    assert actual == expected


def test_hand_strength_two_pair():
    actual = Hand("23432").strength
    expected = 3

    assert actual == expected


def test_hand_strength_one_pair():
    actual = Hand("A23A4").strength
    expected = 2

    assert actual == expected


def test_hand_strength_high_card():
    actual = Hand("23456").strength
    expected = 1

    assert actual == expected


def test_comparison_live():
    stronger = Hand("66686")
    weaker = Hand("222A2")
    assert stronger > weaker


def test_get_ranks():
    rank_5 = Hand("QQQJA")
    rank_4 = Hand("T55J5")
    rank_3 = Hand("KK677")
    rank_2 = Hand("KTJJT")
    rank_1 = Hand("32T3K")
    hands = [rank_5, rank_3, rank_4, rank_2, rank_1]

    expected = {1: rank_1, 2: rank_2, 3: rank_3, 4: rank_4, 5: rank_5}
    actual = get_ranks(hands)

    assert expected == actual


def test_get_winnings():
    rank_5 = Hand("QQQJA", 483)
    rank_4 = Hand("T55J5", 684)
    rank_3 = Hand("KK677", 28)
    rank_2 = Hand("KTJJT", 220)
    rank_1 = Hand("32T3K", 765)
    hands = [rank_5, rank_3, rank_4, rank_2, rank_1]

    ranked_hands = get_ranks(hands)
    expected = 6440
    actual = get_winnings(ranked_hands)

    assert expected == actual


def test_find_answer():
    actual = find_answer("input.test.txt")
    expected = 6440

    assert actual == expected

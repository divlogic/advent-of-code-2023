from functools import total_ordering
from pathlib import Path
from typing import Dict, List

card_strengths = dict(
    [(item, index) for index, item in enumerate(reversed("AKQJT98765432"))]
)


@total_ordering
class Hand:
    def __init__(self, cards: str, bid: str | int | None = None) -> None:
        self.cards: str = cards
        self.bid = int(bid) if bid is not None else None
        self.strength: int = self.get_strength()

    def get_ordered_strength(self) -> str:
        strength = ""
        for character in self.cards:
            strength += str(card_strengths[character]) + " "
        return strength

    def get_strength(self) -> int:
        card_counts = {}
        for card in self.cards:
            card_counts[card] = card_counts.get(card, 0) + 1

        counts = sorted(card_counts.values())
        if counts[-1] == 5:
            return 7
        elif counts[-1] == 4:
            return 6
        elif counts[-1] == 3 and counts[-2] == 2:
            return 5
        elif counts[-1] == 3:
            return 4
        elif counts[-1] == 2 and counts[-2] == 2:
            return 3
        elif counts[-1] == 2:
            return 2
        elif counts[-1] == 1:
            return 1

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.strength < other.strength:
            return True
        elif self.strength > other.strength:
            return False
        else:
            for i in range(0, 5):
                own_strength = card_strengths[self.cards[i]]
                other_strength = card_strengths[other.cards[i]]
                if own_strength < other_strength:
                    return True
                elif own_strength > other_strength:
                    return False

        return False

    def __str__(self) -> str:
        return f"Hand: {self.cards}, Strength: {self.strength}, Bid: {self.bid} {self.get_ordered_strength()}"

    def __repr__(self) -> str:
        return self.__str__()


def get_ranks(hands: List[Hand]) -> Dict[int, Hand]:
    rankings = {}
    sorted_hands = sorted(hands)
    for index, hand in enumerate(sorted_hands):
        rankings[index + 1] = hand
    return rankings


def get_winnings(ranked_hands: Dict[int, Hand]) -> int:
    winnings = 0
    for rank, hand in ranked_hands.items():
        winnings += rank * hand.bid

    return winnings


def find_answer(filename):
    lines = None

    with open(Path(__file__).parents[1] / (filename)) as file:
        lines = file.readlines()

    unranked_hands = []

    for line in lines:
        parsed_data = line.split(" ")
        unranked_hands.append(Hand(parsed_data[0], parsed_data[1]))

    ranked_hands = get_ranks(unranked_hands)

    total_winnings = get_winnings(ranked_hands)

    return total_winnings

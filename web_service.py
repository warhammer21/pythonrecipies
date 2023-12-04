class Card:

    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit):
        self.rank = int(rank)
        self.suit = suit
    def __repr__(self):
        return ("Card(rank={self.rank!r}, "
            "suit={self.suit!r})").format(self=self)
    def to_json(self):
        return {
            "__class__": "Card",
            'rank': self.rank,
            'suit': self.suit}

import random
import json
class Deck:
    SUITS = (
    '\N{black spade suit}',
    '\N{white heart suit}',
    '\N{white diamond suit}',
    '\N{black club suit}',
    )

    def __init__(self, n=1):
        self.n = n
        self.create_deck(self.n)
    def create_deck(self, n=1):
        self.cards = [
            Card(r,s)
            for r in range(1,14)
                for s in self.SUITS
                     for _ in range(n)
        ]
        random.shuffle(self.cards)
        self.offset = 0
    def deal(self, hand_size=5):
        if self.offset + hand_size > len(self.cards):
            self.create_deck(self.n)
        hand = self.cards[self.offset:self.offset+hand_size]
        self.offset += hand_size
        return hand
deck = Deck()
cards = deck.deal(5)
#print(cards)
json_cards = list(card.to_json() for card in deck.deal(5))
print(json.dumps(json_cards, indent=2, sort_keys=True))

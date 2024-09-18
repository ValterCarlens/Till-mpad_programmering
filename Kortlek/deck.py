#skapa en kortlek med hjälp av objektorienterad programmering - använd klasser
import random
import os
os.system("cls")

class Card:
    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.suit} {self.value}"
    
    

    
class Deck:
    def __init__(self, cards=None) -> None:
        if cards == None:
            cards = []
        self.cards = cards

    @staticmethod
    def create_deck():
        cards = []
        suits = ["♠", "♥", "♣", "♦"]
        values = ["Ess", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]

        for suit in range(0, len(suits)):
            for value in range(0, len(values)):
                cards.append(f"{suits[suit]} {values[value]}")

        return cards
    
    def print_cards(deck):
        text = "All cards: "
        for card in deck:
            text += f"{card}, "
        print(text)

    def print_random_card(deck):
        random_card_index = random.randint(0, len(deck))
        print(f"\nRandom card: {deck[random_card_index]}")




deck = Deck.create_deck()
Deck.print_cards(deck)
Deck.print_random_card(deck)
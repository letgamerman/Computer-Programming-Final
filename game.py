"""Blackjack game logic and state management.

This module contains the core game mechanics: dealing cards, calculating hand values,
comparing player/dealer hands, managing bets and balance.
"""

import random
from typing import Tuple, List
from enum import Enum


class Suit(Enum):
    """Card suits."""
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
    """Card ranks and their values."""
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 10)
    QUEEN = ("Q", 10)
    KING = ("K", 10)
    ACE = ("A", 11)

    def __init__(self, display, base_value):
        self.display = display
        self.base_value = base_value


class Card:
    """Represents a single playing card."""

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank.display}{self.suit.value}"

    def get_value(self, allow_ace_as_one: bool = False) -> int:
        """Return card value. Aces are 11 by default, or 1 if allow_ace_as_one."""
        if self.rank == Rank.ACE and allow_ace_as_one:
            return 1
        return self.rank.base_value


class Deck:
    """Represents a deck of 52 cards."""

    def __init__(self):
        self.cards: List[Card] = []
        self._build()

    def _build(self):
        """Build a standard 52-card deck."""
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """Deal a card from the top of the deck."""
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop()

    def remaining(self) -> int:
        """Return number of cards left in deck."""
        return len(self.cards)


def calculate_hand_value(cards: List[Card]) -> Tuple[int, bool]:
    """Calculate the best hand value for a list of cards.

    Returns:
        Tuple of (hand_value: int, has_ace: bool).
        If hand_value > 21, player busts.
        has_ace indicates if an Ace was counted as 11 (soft hand).
    """
    total = sum(card.get_value(allow_ace_as_one=False) for card in cards)
    num_aces = sum(1 for card in cards if card.rank == Rank.ACE)

    has_ace = False
    # Convert Aces from 11 to 1 until total <= 21 or no Aces left
    while total > 21 and num_aces > 0:
        total -= 10  # Convert one Ace from 11 to 1
        num_aces -= 1
        has_ace = True

    if num_aces > 0:
        has_ace = True

    return total, has_ace


def compare_hands(player_total: int, dealer_total: int) -> Tuple[str, str]:
    """Compare player and dealer hands and return result.

    Args:
        player_total: Total value of player's hand.
        dealer_total: Total value of dealer's hand.

    Returns:
        Tuple of (result: str, message: str).
        result is one of: "bust", "win", "lose", "push".
    """
    if not isinstance(player_total, int) or not isinstance(dealer_total, int):
        raise TypeError("Totals must be integers")
    if player_total < 0 or dealer_total < 0:
        raise ValueError("Totals must be non-negative")

    # Player busts
    if player_total > 21:
        return "bust", f"Player busts with {player_total}. Dealer wins."

    # Dealer busts
    if dealer_total > 21:
        return "win", f"Dealer busts with {dealer_total}. Player wins!"

    # Compare totals
    if player_total > dealer_total:
        return "win", f"Player wins: {player_total} vs {dealer_total}."
    if player_total < dealer_total:
        return "lose", f"Dealer wins: {dealer_total} vs {player_total}."

    # Tie
    return "push", f"Push (tie) at {player_total}."


class BlackjackGame:
    """Main blackjack game state and logic."""

    def __init__(self, starting_balance: int = 2000, target_balance: int = 25000, mode: str = "classic"):
        """Initialize the game.

        Args:
            starting_balance: Player's starting chip count.
            target_balance: Target balance to win.
            mode: "practice" (no wagers), "classic" (standard), or "custom" (user-defined).
        """
        self.starting_balance = starting_balance
        self.target_balance = target_balance
        self.mode = mode  # practice, classic, or custom
        self.balance = starting_balance
        self.current_bet = 0

        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand: List[Card] = []
        self.dealer_hand: List[Card] = []

        self.game_state = "betting"  # betting, dealing, playing, result, won, lost, out_of_money
        self.result_message = ""

    def reset_for_new_hand(self):
        """Reset hands and state for a new round."""
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.game_state = "betting"
        self.result_message = ""
        self.current_bet = 0

        # Reshuffle if deck is getting low
        if self.deck.remaining() < 10:
            self.deck = Deck()
            self.deck.shuffle()

    def place_bet(self, amount: int = 0) -> Tuple[bool, str]:
        """Place a bet for the current hand.

        Returns:
            Tuple of (success: bool, message: str).
        """
        # In practice mode, no bet needed
        if self.mode == "practice":
            self.current_bet = 0
            self.game_state = "dealing"
            return True, "Practice mode: Dealing cards..."

        if amount <= 0:
            return False, "Bet must be greater than 0."
        if amount > self.balance:
            return False, f"Insufficient balance. You have {self.balance}."
        if self.balance <= 0:
            return False, "Game over. Reset balance to play again."

        self.current_bet = amount
        self.game_state = "dealing"
        return True, f"Bet placed: {amount}. Dealing cards..."

    def deal_initial_hands(self):
        """Deal two cards each to player and dealer."""
        self.player_hand = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand = [self.deck.deal(), self.deck.deal()]
        
        # Check for natural blackjack (21 on first two cards)
        player_total, _ = calculate_hand_value(self.player_hand)
        dealer_total, _ = calculate_hand_value(self.dealer_hand)
        
        if player_total == 21 and dealer_total != 21:
            # Player has blackjack, dealer doesn't
            self.game_state = "result"
            self.result_message = "Natural Blackjack! Player wins!"
            self.balance += int(self.current_bet * 1.5)  # 3:2 payout
        elif dealer_total == 21 and player_total != 21:
            # Dealer has blackjack, player doesn't
            self.game_state = "result"
            self.result_message = "Dealer has Blackjack! Dealer wins."
            self.balance -= self.current_bet
        elif player_total == 21 and dealer_total == 21:
            # Both have blackjack
            self.game_state = "result"
            self.result_message = "Both have Blackjack! Push."
        else:
            self.game_state = "playing"

    def player_hit(self) -> Tuple[str, str]:
        """Player takes another card.

        Returns:
            Tuple of (action_result: str, message: str).
            action_result: "hit", "bust", or "invalid".
        """
        if self.game_state != "playing":
            return "invalid", "Cannot hit now."

        self.player_hand.append(self.deck.deal())
        player_total, _ = calculate_hand_value(self.player_hand)

        if player_total > 21:
            self.game_state = "result"
            result, message = compare_hands(player_total, 0)  # Force bust
            self.result_message = f"Player busts with {player_total}. Dealer wins."
            self.balance -= self.current_bet
            return "bust", self.result_message

        return "hit", f"Hit! New total: {player_total}"

    def player_stand(self) -> Tuple[str, str]:
        """Player stands; dealer plays out their hand.

        Returns:
            Tuple of (action_result: str, message: str).
            action_result: "stand".
        """
        if self.game_state != "playing":
            return "invalid", "Cannot stand now."

        # Dealer plays: hits until 17 or higher
        while True:
            dealer_total, _ = calculate_hand_value(self.dealer_hand)
            if dealer_total >= 17:
                break
            self.dealer_hand.append(self.deck.deal())

        # Compare hands
        player_total, _ = calculate_hand_value(self.player_hand)
        dealer_total, _ = calculate_hand_value(self.dealer_hand)
        result, message = compare_hands(player_total, dealer_total)

        # Update balance
        if result == "win":
            self.balance += self.current_bet
        elif result == "lose":
            self.balance -= self.current_bet
        # "push" and "bust" already handled

        self.game_state = "result"
        self.result_message = message

        # Check win/loss conditions
        if self.balance >= self.target_balance:
            self.game_state = "won"
        elif self.balance <= 0:
            self.game_state = "out_of_money"

        return "stand", message

    def get_player_hand_str(self) -> str:
        """Return player's hand as a formatted string."""
        cards_str = ", ".join(str(card) for card in self.player_hand)
        total, has_ace = calculate_hand_value(self.player_hand)
        soft_str = " (soft)" if has_ace else ""
        return f"Player: {cards_str} = {total}{soft_str}"

    def get_dealer_hand_str(self, hide_hole_card: bool = False) -> str:
        """Return dealer's hand as a formatted string.

        Args:
            hide_hole_card: If True, hide the dealer's second card (for playing phase).
        """
        if hide_hole_card and len(self.dealer_hand) >= 2:
            cards_str = f"{self.dealer_hand[0]}, [hidden]"
            return f"Dealer: {cards_str}"
        else:
            cards_str = ", ".join(str(card) for card in self.dealer_hand)
            total, has_ace = calculate_hand_value(self.dealer_hand)
            soft_str = " (soft)" if has_ace else ""
            return f"Dealer: {cards_str} = {total}{soft_str}"

    def reset_balance_on_broke(self):
        """Reset player balance to starting amount when broke."""
        self.balance = self.starting_balance
        self.game_state = "betting"


if __name__ == "__main__":
    # Quick test of game logic
    game = BlackjackGame()
    print("Testing Blackjack Game Logic...")
    print(f"Starting balance: {game.balance}")

    # Test betting and dealing
    success, msg = game.place_bet(100)
    print(f"Bet: {msg}")

    game.deal_initial_hands()
    print(game.get_player_hand_str())
    print(game.get_dealer_hand_str(hide_hole_card=True))

    print("\nGame initialized successfully!")

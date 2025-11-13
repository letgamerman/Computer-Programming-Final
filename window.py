import pygame_cards-0.1


def compare_totals(player_total: int, dealer_total: int) -> Tuple[str, str]:
    """Compare blackjack totals and return (result, message).

    Result is one of: 'bust', 'win', 'lose', 'push'.

    Raises:
        TypeError: if inputs are not ints
        ValueError: if inputs are negative
    """
    if not isinstance(player_total, int) or not isinstance(dealer_total, int):
        raise TypeError("Totals must be integers")
    if player_total < 0 or dealer_total < 0:
        raise ValueError("Totals must be non-negative")

    # 3A: player busts
    if player_total > 21:
        return "bust", f"Player busts with {player_total}. Dealer wins."

    # dealer busts
    if dealer_total > 21:
        return "win", f"Dealer busts with {dealer_total}. Player wins."

    # compare totals
    if player_total > dealer_total:
        return "win", f"Player wins: {player_total} vs {dealer_total}."
    if player_total < dealer_total:
        return "lose", f"Dealer wins: {dealer_total} vs {player_total}."

    # tie
    return "push", f"Push (tie) at {player_total}."


def _run_demo() -> None:
    """Small demo / test harness that prints a few example outcomes."""
    examples = [
        (22, 18),  # player bust
        (20, 22),  # dealer bust
        (20, 19),  # player wins
        (18, 20),  # dealer wins
        (21, 21),  # push
    ]
    for p, d in examples:
        result, msg = compare_totals(p, d)
        print(f"player={p:2d}, dealer={d:2d} -> {result}: {msg}")


if __name__ == "__main__":
    _run_demo()


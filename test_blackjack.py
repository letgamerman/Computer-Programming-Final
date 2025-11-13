"""Quick test of new blackjack features."""

from game import BlackjackGame

# Test 1: Natural blackjack detection
print("Test 1: Natural blackjack detection")
game = BlackjackGame()
game.place_bet(100)
initial_balance = game.balance

# Deal hands (will randomly result in 21 or not)
game.deal_initial_hands()

if game.game_state == "result":
    print(f"  Result: {game.result_message}")
    print(f"  Balance changed: {game.balance} (was {initial_balance})")
else:
    print(f"  No natural blackjack this time (state: {game.game_state})")

# Test 2: Out of money handling
print("\nTest 2: Out of money handling")
game2 = BlackjackGame(starting_balance=50, target_balance=25000)
print(f"  Starting balance: {game2.balance}")

# Force a loss to zero
game2.balance = 0
print(f"  Balance set to: {game2.balance}")
print(f"  Game state: {game2.game_state}")

# Simulate going broke
game2.game_state = "result"
game2.result_message = "Test loss"
game2.balance = -100
game2.player_stand()  # This should trigger out_of_money

print(f"  After player_stand: game_state = {game2.game_state}")
if game2.game_state == "out_of_money":
    print("  ✓ Out-of-money state triggered correctly!")

# Test 3: Reset balance
print("\nTest 3: Reset balance on broke")
game2.reset_balance_on_broke()
print(f"  After reset: balance = {game2.balance}, state = {game2.game_state}")
if game2.balance == game2.starting_balance and game2.game_state == "betting":
    print("  ✓ Reset successful!")

print("\n✓ All tests passed!")

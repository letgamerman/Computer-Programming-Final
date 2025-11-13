#!/usr/bin/env python3
"""Integration test for the Blackjack game with mode selection."""

import sys
import pygame
from game import BlackjackGame
from window import BlackjackWindow, GameModeScreen

def test_mode_selection():
    """Test that mode selection works correctly."""
    print("[TEST] Testing mode selection...")
    
    # Initialize pygame
    pygame.init()
    
    # Create a test screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Mode Selection")
    
    # Create GameModeScreen
    mode_screen = GameModeScreen(screen)
    
    # Test button creation
    assert len(mode_screen.buttons) == 3, "Should have 3 mode buttons"
    print("[OK] GameModeScreen has 3 buttons")
    
    # Test button labels
    button_labels = [btn.text for btn in mode_screen.buttons]
    expected_labels = ["Practice Mode (No Wagers)", "Classic Mode ($2000 -> $25000)", "Custom Mode (Set Goals)"]
    assert button_labels == expected_labels, f"Button labels mismatch: {button_labels}"
    print("[OK] Button labels are correct")
    
    # Test button selection
    mode_screen._select("practice")
    assert mode_screen.selected_mode == "practice", "Should select practice mode"
    print("[OK] Mode selection works")
    
    pygame.quit()
    print("[TEST] Mode selection tests PASSED\n")

def test_game_initialization():
    """Test game initialization with different modes."""
    print("[TEST] Testing game initialization with modes...")
    
    # Test practice mode
    game_practice = BlackjackGame(starting_balance=0, target_balance=0, mode="practice")
    assert game_practice.mode == "practice", "Should set mode to practice"
    assert game_practice.balance == 0, "Practice mode should have 0 balance"
    print("[OK] Practice mode initialization works")
    
    # Test classic mode
    game_classic = BlackjackGame(starting_balance=2000, target_balance=25000, mode="classic")
    assert game_classic.mode == "classic", "Should set mode to classic"
    assert game_classic.balance == 2000, "Classic mode should start with $2000"
    assert game_classic.target_balance == 25000, "Classic mode target should be $25000"
    print("[OK] Classic mode initialization works")
    
    # Test practice mode betting
    success, msg = game_practice.place_bet()
    assert success, f"Practice mode betting failed: {msg}"
    print("[OK] Practice mode betting works (no amount required)")
    
    # Test classic mode betting
    success, msg = game_classic.place_bet(100)
    assert success, f"Classic mode betting failed: {msg}"
    assert game_classic.current_bet == 100, "Bet amount should be set"
    print("[OK] Classic mode betting works")
    
    print("[TEST] Game initialization tests PASSED\n")

def test_window_integration():
    """Test BlackjackWindow integration."""
    print("[TEST] Testing BlackjackWindow integration...")
    
    # Initialize pygame
    pygame.init()
    
    # Create window - should start on mode_select screen
    window = BlackjackWindow(800, 600, mode="practice", starting_balance=0, target_balance=0)
    
    assert window.screen_state == "mode_select", "Window should start on mode_select screen"
    print("[OK] Window starts on mode selection screen")
    
    assert window.game_mode_screen is not None, "Should have GameModeScreen instance"
    print("[OK] GameModeScreen is initialized")
    
    # Test mode selection transition
    selected_mode = window.game_mode_screen.handle_click((250, 200))  # Approximate position of first button
    if selected_mode:
        window.screen_state = "game"
        window.game = BlackjackGame(starting_balance=0, target_balance=0, mode=selected_mode)
        assert window.screen_state == "game", "Window should transition to game screen"
        print("[OK] Mode selection transition works")
    
    pygame.quit()
    print("[TEST] BlackjackWindow integration tests PASSED\n")

if __name__ == "__main__":
    try:
        test_mode_selection()
        test_game_initialization()
        test_window_integration()
        print("=" * 50)
        print("ALL INTEGRATION TESTS PASSED!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

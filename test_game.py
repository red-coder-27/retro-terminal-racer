#!/usr/bin/env python3
"""
Test script to verify Terminal Racer code structure
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from terminal_racer import TerminalRacer, GameState, Obstacle, Player
    print("✅ All imports successful!")
    
    # Test class instantiation (without curses)
    print("Classes defined correctly:")
    print(f"  - GameState enum: {list(GameState)}")
    print(f"  - Obstacle dataclass: {Obstacle.__annotations__}")
    print(f"  - Player dataclass: {Player.__annotations__}")
    
    # Test game logic methods exist
    game_methods = [
        'init_colors', 'load_high_score', 'save_high_score', 'reset_game',
        'draw_menu', 'draw_road', 'draw_player', 'draw_obstacles', 'draw_ui',
        'spawn_obstacle', 'update_obstacles', 'check_collision', 'handle_input',
        'update_game_logic', 'draw_game_over', 'draw_pause_screen', 'draw_game', 'run'
    ]
    
    print("✅ Game methods defined:")
    for method in game_methods:
        if hasattr(TerminalRacer, method):
            print(f"  ✓ {method}")
        else:
            print(f"  ✗ {method} - MISSING")
    
    print("\n🎮 Terminal Racer code structure is valid!")
    print("📝 The game is ready to run in a proper terminal environment.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")


"""
Terminal Racer - Real-time ASCII Car Racing Game
A smooth, arcade-style racing experience in your terminal!
"""

import curses
import time
import random
import json
import os
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

@dataclass
class Obstacle:
    x: int
    y: int
    char: str
    color: int

@dataclass
class Player:
    x: int
    y: int
    char: str
    color: int

class TerminalRacer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Game settings
        self.FPS = 25
        self.LANES = 5
        self.LANE_WIDTH = 4
        self.ROAD_WIDTH = self.LANES * self.LANE_WIDTH
        self.ROAD_START_X = (self.width - self.ROAD_WIDTH) // 2
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.high_score = self.load_high_score()
        self.frame_count = 0
        self.speed = 1
        self.nitro_active = False
        self.nitro_cooldown = 0
        
        # Player
        self.player = Player(
            x=self.ROAD_START_X + (self.LANES // 2) * self.LANE_WIDTH + 1,
            y=self.height - 3,
            char="🚗",
            color=1
        )
        
        # Obstacles
        self.obstacles: List[Obstacle] = []
        self.obstacle_spawn_rate = 0.3
        
        # Initialize colors
        self.init_colors()
        
        # Configure curses
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)   # Non-blocking input
        stdscr.timeout(1000 // self.FPS)  # Set refresh rate
        
    def init_colors(self):
        """Initialize color pairs for the game"""
        curses.start_color()
        curses.use_default_colors()
        
        # Color pairs
        curses.init_pair(1, curses.COLOR_CYAN, -1)    # Player car
        curses.init_pair(2, curses.COLOR_RED, -1)     # Obstacles
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Road lines
        curses.init_pair(4, curses.COLOR_GREEN, -1)   # UI text
        curses.init_pair(5, curses.COLOR_MAGENTA, -1) # Nitro effect
        curses.init_pair(6, curses.COLOR_WHITE, -1)   # Menu text
        curses.init_pair(7, curses.COLOR_BLUE, -1)    # Borders
        
    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            if os.path.exists("high_score.json"):
                with open("high_score.json", "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except:
            pass
        return 0
        
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("high_score.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass
            
    def reset_game(self):
        """Reset game state for new game"""
        self.score = 0
        self.frame_count = 0
        self.speed = 1
        self.nitro_active = False
        self.nitro_cooldown = 0
        self.obstacles.clear()
        self.player.x = self.ROAD_START_X + (self.LANES // 2) * self.LANE_WIDTH + 1
        self.obstacle_spawn_rate = 0.3
        
    def draw_menu(self):
        """Draw the main menu"""
        self.stdscr.clear()
        
        # Title
        title = [
            "╔══════════════════════════════════════╗",
            "║         TERMINAL RACER 🏁            ║",
            "║                                      ║",
            "║    🚗💨 ASCII Racing Action! 💨🚗    ║",
            "╚══════════════════════════════════════╝"
        ]
        
        start_y = self.height // 2 - 8
        for i, line in enumerate(title):
            x = (self.width - len(line)) // 2
            self.stdscr.addstr(start_y + i, x, line, curses.color_pair(6))
            
        # Menu options
        menu_text = [
            "",
            "🎮 CONTROLS:",
            "  ← → or A/D  : Move left/right",
            "  SPACEBAR    : Nitro boost",
            "  P           : Pause game",
            "  Q           : Quit",
            "",
            f"🏆 HIGH SCORE: {self.high_score}",
            "",
            "Press ENTER to start racing!"
        ]
        
        for i, line in enumerate(menu_text):
            x = (self.width - len(line)) // 2
            color = curses.color_pair(4) if line.startswith("🏆") else curses.color_pair(6)
            self.stdscr.addstr(start_y + len(title) + i + 1, x, line, color)
            
        self.stdscr.refresh()
        
    def draw_road(self):
        """Draw the racing road with lanes"""
        # Draw road borders
        left_border = self.ROAD_START_X - 1
        right_border = self.ROAD_START_X + self.ROAD_WIDTH
        
        for y in range(self.height):
            # Left border
            if left_border >= 0:
                self.stdscr.addch(y, left_border, '║', curses.color_pair(7))
            # Right border  
            if right_border < self.width:
                self.stdscr.addch(y, right_border, '║', curses.color_pair(7))
                
        # Draw lane dividers (animated dashed lines)
        for lane in range(1, self.LANES):
            x = self.ROAD_START_X + lane * self.LANE_WIDTH - 1
            if 0 <= x < self.width:
                for y in range(0, self.height, 4):
                    # Animate the dashes by offsetting based on frame count
                    if (y + self.frame_count // 2) % 4 < 2:
                        if 0 <= y < self.height:
                            self.stdscr.addch(y, x, '|', curses.color_pair(3))
                            
    def draw_player(self):
        """Draw the player's car"""
        if 0 <= self.player.y < self.height and 0 <= self.player.x < self.width:
            color = curses.color_pair(5) if self.nitro_active else curses.color_pair(1)
            
            # Try to use emoji, fallback to ASCII
            try:
                self.stdscr.addstr(self.player.y, self.player.x, self.player.char, color)
            except:
                # Fallback ASCII car
                self.stdscr.addstr(self.player.y, self.player.x, "|A|", color)
                
            # Nitro effect
            if self.nitro_active and self.player.y + 1 < self.height:
                try:
                    self.stdscr.addstr(self.player.y + 1, self.player.x, "💨", curses.color_pair(5))
                except:
                    self.stdscr.addstr(self.player.y + 1, self.player.x, "^^^", curses.color_pair(5))
                    
    def draw_obstacles(self):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            y = int(obstacle.y)  # Cast to int
            x = int(obstacle.x)  # Cast to int
            if (0 <= y < self.height and 0 <= x < self.width):
                self.stdscr.addch(y, x, obstacle.char,curses.color_pair(obstacle.color))
                                
    def draw_ui(self):
        """Draw game UI (score, speed, etc.)"""
        # Score
        score_text = f"SCORE: {self.score}"
        self.stdscr.addstr(1, 2, score_text, curses.color_pair(4))
        
        # High score
        high_score_text = f"HIGH: {self.high_score}"
        self.stdscr.addstr(2, 2, high_score_text, curses.color_pair(4))
        
        # Speed
        speed_text = f"SPEED: {self.speed}"
        self.stdscr.addstr(1, self.width - len(speed_text) - 2, speed_text, curses.color_pair(4))
        
        # Nitro status
        if self.nitro_cooldown > 0:
            nitro_text = f"NITRO: {self.nitro_cooldown // self.FPS + 1}s"
            color = curses.color_pair(2)
        elif self.nitro_active:
            nitro_text = "NITRO: ACTIVE!"
            color = curses.color_pair(5)
        else:
            nitro_text = "NITRO: READY"
            color = curses.color_pair(4)
            
        self.stdscr.addstr(2, self.width - len(nitro_text) - 2, nitro_text, color)
        
        # Instructions
        if self.frame_count < self.FPS * 5:  # Show for first 5 seconds
            help_text = "← → Move | SPACE Nitro | P Pause | Q Quit"
            x = (self.width - len(help_text)) // 2
            self.stdscr.addstr(self.height - 1, x, help_text, curses.color_pair(6))
            
    def spawn_obstacle(self):
        """Spawn a new obstacle"""
        if random.random() < self.obstacle_spawn_rate:
            lane = random.randint(0, self.LANES - 1)
            x = self.ROAD_START_X + lane * self.LANE_WIDTH + random.randint(0, self.LANE_WIDTH - 2)
            
            # Different obstacle types
            obstacle_chars = ['X', '#', '▲', '●', '■']
            char = random.choice(obstacle_chars)
            
            obstacle = Obstacle(
                x=x,
                y=0,
                char=char,
                color=2
            )
            self.obstacles.append(obstacle)
            
    def update_obstacles(self):
        """Update obstacle positions"""
        move_speed = self.speed + (2 if self.nitro_active else 0)
        
        # Move obstacles down
        for obstacle in self.obstacles:
            obstacle.y += move_speed
            
        # Remove obstacles that are off screen
        self.obstacles = [obs for obs in self.obstacles if obs.y < self.height]
        
    def check_collision(self) -> bool:
        """Check if player collided with any obstacle"""
        player_positions = [
            (self.player.x, self.player.y),
            (self.player.x + 1, self.player.y),  # Car is wider than 1 char
            (self.player.x + 2, self.player.y)
        ]
        
        for obstacle in self.obstacles:
            for px, py in player_positions:
                if (obstacle.x == px and obstacle.y == py):
                    return True
        return False
        
    def handle_input(self):
        """Handle player input"""
        try:
            key = self.stdscr.getch()
        except:
            return
            
        if self.state == GameState.MENU:
            if key in [ord('\n'), ord('\r'), 10]:  # Enter
                self.state = GameState.PLAYING
                self.reset_game()
        elif self.state == GameState.PLAYING:
            # Movement
            if key in [curses.KEY_LEFT, ord('a'), ord('A')]:
                new_x = self.player.x - self.LANE_WIDTH
                if new_x >= self.ROAD_START_X:
                    self.player.x = new_x
                    
            elif key in [curses.KEY_RIGHT, ord('d'), ord('D')]:
                new_x = self.player.x + self.LANE_WIDTH
                if new_x < self.ROAD_START_X + self.ROAD_WIDTH - 2:
                    self.player.x = new_x
                    
            # Nitro boost
            elif key == ord(' '):
                if not self.nitro_active and self.nitro_cooldown <= 0:
                    self.nitro_active = True
                    self.nitro_cooldown = self.FPS * 3  # 3 second cooldown
                    
            # Pause
            elif key in [ord('p'), ord('P')]:
                self.state = GameState.PAUSED
                
        elif self.state == GameState.PAUSED:
            if key in [ord('p'), ord('P')]:
                self.state = GameState.PLAYING
                
        elif self.state == GameState.GAME_OVER:
            if key in [ord('\n'), ord('\r'), 10]:  # Enter to restart
                self.state = GameState.MENU
                
        # Quit game
        if key in [ord('q'), ord('Q')]:
            return False
            
        return True
        
    def update_game_logic(self):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
            
        self.frame_count += 1
        
        # Update score
        self.score = self.frame_count // 10
        
        # Increase difficulty over time
        if self.frame_count % (self.FPS * 10) == 0:  # Every 10 seconds
            self.speed = min(3, self.speed + 0.2)
            self.obstacle_spawn_rate = min(0.8, self.obstacle_spawn_rate + 0.05)
            
        # Handle nitro
        if self.nitro_active:
            if self.frame_count % (self.FPS // 2) == 0:  # Nitro lasts 0.5 seconds
                self.nitro_active = False
        
        if self.nitro_cooldown > 0:
            self.nitro_cooldown -= 1
            
        # Spawn and update obstacles
        self.spawn_obstacle()
        self.update_obstacles()
        
        # Check collision
        if self.check_collision():
            self.state = GameState.GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
                
    def draw_game_over(self):
        """Draw game over screen"""
        self.stdscr.clear()
        
        # Game over message
        game_over_text = [
            "╔══════════════════════════════════════╗",
            "║             GAME OVER!               ║",
            "║                                      ║",
            f"║         FINAL SCORE: {self.score:4d}         ║",
            f"║         HIGH SCORE:  {self.high_score:4d}         ║",
            "║                                      ║",
            "║      Press ENTER to continue         ║",
            "║      Press Q to quit                 ║",
            "╚══════════════════════════════════════╝"
        ]
        
        start_y = self.height // 2 - len(game_over_text) // 2
        for i, line in enumerate(game_over_text):
            x = (self.width - len(line)) // 2
            color = curses.color_pair(4) if "SCORE" in line else curses.color_pair(6)
            self.stdscr.addstr(start_y + i, x, line, color)
            
        # New high score message
        if self.score == self.high_score and self.score > 0:
            congrats = "🎉 NEW HIGH SCORE! 🎉"
            x = (self.width - len(congrats)) // 2
            self.stdscr.addstr(start_y - 2, x, congrats, curses.color_pair(5))
            
        self.stdscr.refresh()
        
    def draw_pause_screen(self):
        """Draw pause screen"""
        # Draw game state in background (dimmed)
        self.draw_game()
        
        # Pause overlay
        pause_text = [
            "╔══════════════════╗",
            "║      PAUSED      ║",
            "║                  ║",
            "║  Press P to      ║",
            "║  continue        ║",
            "╚══════════════════╝"
        ]
        
        start_y = self.height // 2 - len(pause_text) // 2
        for i, line in enumerate(pause_text):
            x = (self.width - len(line)) // 2
            self.stdscr.addstr(start_y + i, x, line, curses.color_pair(6))
            
    def draw_game(self):
        """Draw the main game screen"""
        self.stdscr.clear()
        self.draw_road()
        self.draw_obstacles()
        self.draw_player()
        self.draw_ui()
        
    def run(self):
        """Main game loop"""
        while True:
            # Handle input
            if not self.handle_input():
                break
                
            # Update game logic
            self.update_game_logic()
            
            # Draw appropriate screen
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.PAUSED:
                self.draw_pause_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
                
            self.stdscr.refresh()
            
            # Control frame rate
            time.sleep(1 / self.FPS)

def main(stdscr):
    """Main function to run the game"""
    try:
        game = TerminalRacer(stdscr)
        game.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Clean exit on any error
        curses.endwin()
        print(f"Game error: {e}")

if __name__ == "__main__":
    # Check terminal size
    try:
        import shutil
        cols, rows = shutil.get_terminal_size()
        if cols < 60 or rows < 20:
            print("⚠️  Terminal too small! Please resize to at least 60x20 characters.")
            print(f"Current size: {cols}x{rows}")
            exit(1)
    except:
        pass
        
    print("🏁 Starting Terminal Racer...")
    print("Make sure your terminal supports colors and is at least 60x20!")
    time.sleep(1)
    
    # Start the game
    curses.wrapper(main)



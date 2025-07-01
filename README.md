# 🏁 Terminal Racer

A smooth, arcade-style ASCII car racing game that runs entirely in your terminal! Experience the thrill of retro racing with modern Python programming.
Developed as a creative submission for the Amazon Q Dev CLI Hackathon, Terminal Racer showcases how AI-assisted development and classic programming can come together to build nostalgic games with a modern twist
## 🎮 Features

- **Real-time Racing Action**: Smooth 25 FPS gameplay with responsive controls
- **Dynamic Difficulty**: Speed and obstacle density increase over time
- **Nitro Boost System**: Strategic power-ups with cooldown mechanics
- **Persistent High Scores**: Your best scores are saved between sessions
- **Multiple Game States**: Menu, gameplay, pause, and game over screens
- **Colorful ASCII Graphics**: Beautiful terminal-based visuals with emoji support
- **Responsive Design**: Adapts to different terminal sizes
- **Collision Detection**: Precise hit detection for challenging gameplay

## 🚗 Gameplay

Navigate your car through increasingly difficult traffic while collecting points:

- **Objective**: Avoid obstacles and survive as long as possible
- **Scoring**: Points increase based on survival time
- **Power-ups**: Use nitro boost to speed through tight spots
- **Difficulty**: Game gets faster and more challenging over time

## 🎯 Controls

| Key | Action |
|-----|--------|
| `←` `→` or `A` `D` | Move left/right between lanes |
| `SPACEBAR` | Activate nitro boost |
| `P` | Pause/unpause game |
| `Q` | Quit game |
| `ENTER` | Start game / Continue after game over |

## 🛠 Requirements

- **Python 3.6+** with `curses` module (included in most Python installations)
- **Terminal**: At least 60x20 characters
- **Color Support**: Terminal that supports ANSI colors
- **Unicode Support**: For emoji characters (optional, ASCII fallback available)

## 🚀 Installation & Running
# For linux & mac os :
1. **Clone or download** the `terminal_racer.py` file
2. **Make it executable** (optional):
   ```bash
   chmod +x terminal_racer.py
   ```
3. **Run the game**:
   ```bash
   python3 terminal_racer.py
   # or if executable:
   ./terminal_racer.py
   
# for Windows os :   ```
1. **Clone or download** the `terminal_racer.py` file
2. **Open Command Prompt or PowerShell** in the file's directory
3. **Run the game**:
      cmd 
    python terminal_racer.py


## 🏗 Code Architecture

The game is built with clean, modular Python code:

### Core Classes

- **`GameState`**: Enum managing different game states (menu, playing, paused, game over)
- **`Player`**: Dataclass representing the player's car
- **`Obstacle`**: Dataclass for obstacles on the road
- **`TerminalRacer`**: Main game class handling all logic and rendering

### Key Systems

- **Rendering Engine**: Efficient curses-based drawing with color support
- **Input System**: Non-blocking keyboard input handling
- **Physics**: Collision detection and movement mechanics
- **Game Loop**: Fixed timestep game loop at 25 FPS
- **State Management**: Clean state transitions between game modes
- **Persistence**: JSON-based high score saving

## 🎨 Technical Highlights

### Smooth Animation
```python
# Animated lane dividers
if (y + self.frame_count // 2) % 4 < 2:
    self.stdscr.addch(y, x, '|', curses.color_pair(3))
```

### Dynamic Difficulty Scaling
```python
# Increase difficulty every 10 seconds
if self.frame_count % (self.FPS * 10) == 0:
    self.speed = min(3, self.speed + 0.2)
    self.obstacle_spawn_rate = min(0.8, self.obstacle_spawn_rate + 0.05)
```

### Robust Error Handling
```python
# Graceful emoji fallback
try:
    self.stdscr.addstr(self.player.y, self.player.x, "🚗", color)
except:
    self.stdscr.addstr(self.player.y, self.player.x, "|A|", color)
```

## 🐛 Troubleshooting

### Terminal Too Small
```
⚠️ Terminal too small! Please resize to at least 60x20 characters.
```
**Solution**: Resize your terminal window or use a smaller font size.

### Color Issues
If colors don't display correctly:
- Ensure your terminal supports ANSI colors
- Try different terminal applications (iTerm2, Windows Terminal, etc.)

### Curses Errors
If you get curses-related errors:
- Make sure you're running in a proper terminal (not an IDE console)
- Try different terminal emulators
- Ensure Python's curses module is properly installed

## 🎯 Game Tips

1. **Lane Strategy**: Stay in center lanes for maximum escape options
2. **Nitro Timing**: Save nitro for emergency situations
3. **Pattern Recognition**: Learn obstacle spawn patterns
4. **Smooth Movement**: Don't panic-move; plan your lane changes
5. **Score Focus**: Survival time is everything - avoid risky moves

## 🔧 Customization

Easy modifications you can make:

### Adjust Difficulty
```python
self.FPS = 30  # Faster gameplay
self.obstacle_spawn_rate = 0.5  # More obstacles
```

### Change Visuals
```python
obstacle_chars = ['💥', '🚧', '⚠️', '🛑']  # Different obstacles
self.player.char = "🏎️"  # Different car
```

### Modify Controls
```python
# Add WASD support
if key in [ord('w'), ord('W')]:
    # Add boost or jump mechanic
```

## 📊 Performance

- **Memory Usage**: ~2-5 MB
- **CPU Usage**: Minimal (single-threaded)
- **Frame Rate**: Stable 25 FPS
- **Startup Time**: < 1 second

## 🏆 High Score System

Scores are automatically saved to `high_score.json` in the same directory as the game. The file format:

```json
{
  "high_score": 0
}
```

## 🤝 Contributing

This game demonstrates several programming concepts:
- Object-oriented design
- Game loop architecture
- Terminal graphics programming
- State management
- File I/O and persistence
- Error handling and graceful degradation

Feel free to extend it with:
- Multiple car types
- Power-up items
- Sound effects (terminal beeps)
- Multiplayer support
- Level progression
- Achievement system

## 📜 License

This code is provided as-is for educational and entertainment purposes. Feel free to modify, distribute, and learn from it!

---

**Happy Racing! 🏁**

*May your reflexes be quick and your high scores be high!*

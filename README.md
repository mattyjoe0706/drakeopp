# Drake vs The Opps - 2D Action Platformer

A humorous 2D action platformer game where Drake battles his "opps" (opponents) across multiple levels. The game is based on rap beefs but avoids promoting real-life violence - it's all in good fun!

## Features

### Current (Level 1: Drake vs The Weeknd)
- **Player Character**: Drake with mic-bat weapon
- **Movement**: Left/Right movement, jumping, shooting
- **Enemy AI**: The Weeknd with multiple attack patterns
- **Platforming**: Multi-level stage with colored platforms
- **Health System**: Health bars for both player and enemies
- **Projectile Combat**: Different projectile types for each character
- **Sound System**: Placeholder sound effects (expandable)
- **Game States**: Playing, paused, game over, level complete

### Planned Features
- Additional boss characters (Future, Rick Ross, Pusha T, Kendrick Lamar)
- More levels with unique themes
- Power-ups and special attacks
- Actual sound effects and music
- Better sprite graphics
- Story mode with cutscenes

## Controls

- **Movement**: WASD or Arrow Keys
- **Jump**: SPACE, W, or UP arrow
- **Shoot**: X or J
- **Pause**: P
- **Restart**: R (when game over or level complete)
- **Quit**: ESC

## Installation

1. Install Python 3.7+ if not already installed
2. Install pygame:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Game Structure

```
game/
├── __init__.py
├── settings.py           # Game constants and configuration
├── game_manager.py       # Main game coordination
├── entities/
│   ├── __init__.py
│   ├── base_entity.py    # Base class for all game objects
│   ├── player.py         # Drake player character
│   ├── enemies.py        # Enemy/boss characters
│   └── projectile.py     # Bullet/attack system
├── levels/
│   ├── __init__.py
│   ├── level_base.py     # Base level class
│   └── level_one.py      # Level 1: Drake vs The Weeknd
└── audio/
    ├── __init__.py
    └── sound_manager.py   # Sound system (placeholder)
```

## Character Descriptions

### Drake (Player)
- **Color**: Blue rectangle with yellow mic-bat
- **Health**: 100 HP
- **Weapon**: Mic projectiles (yellow with sparkle effect)
- **Speed**: Medium movement, good jump height

### The Weeknd (Level 1 Boss)
- **Color**: Pink rectangle
- **Health**: 200 HP
- **Weapon**: Musical note projectiles (pink)
- **AI**: Multiple attack patterns (single shot, triple shot, wave shot)
- **Movement**: Horizontal patrol with direction changes

### Future (Planned)
- **Color**: Purple rectangle
- **Weapon**: Diamond projectiles (expensive attacks)
- **Style**: Fast hit-and-run tactics

### Rick Ross (Planned)
- **Color**: Orange rectangle
- **Weapon**: Flame projectiles
- **Style**: Tank-like, high health, slow but powerful

## Adding New Content

### Adding a New Enemy
1. Create a new class in `game/entities/enemies.py` inheriting from `BaseEnemy`
2. Implement the `update_ai(self, dt)` method for custom behavior
3. Customize appearance in the `render()` method
4. Add to level by importing and spawning in level file

### Adding a New Level
1. Create a new file in `game/levels/` inheriting from `BaseLevel`
2. Override `create_platforms()` for custom level geometry
3. Set custom spawn points in `__init__()`
4. Add level-specific logic in `update()` and `render_ui()`
5. Add level to game manager

### Adding Sound Effects
1. Place audio files in a `sounds/` directory
2. Use `sound_manager.load_sound("name", "path/to/file.wav")` 
3. Play with `sound_manager.play_sound("name")`

## Technical Notes

- Built with Python and Pygame
- Uses delta-time for frame-rate independent movement
- Modular design for easy expansion
- Object-oriented architecture with inheritance
- Collision detection using pygame rectangles
- Simple AI state machines for enemies

## Humor and Style

The game maintains a lighthearted tone around rap culture and beefs:
- Colorful placeholder sprites with character names
- Musical-themed attacks (notes, mics, etc.)
- Fun victory messages
- No realistic violence - just playful combat

## Development Status

**Current**: Basic playable Level 1 complete
**Next**: Add more enemies and levels, improve graphics, add actual audio

This is a foundation that can be expanded with more features, better graphics, and additional content!
"""
Game settings and constants
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
GAME_TITLE = "Drake vs The Opps"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Physics
GRAVITY = 1000  # pixels per second squared
TERMINAL_VELOCITY = 800  # max falling speed
JUMP_STRENGTH = -400  # negative for upward movement
PLAYER_SPEED = 300  # horizontal movement speed
PROJECTILE_SPEED = 500

# Game mechanics
PLAYER_MAX_HEALTH = 100
BOSS_MAX_HEALTH = 200
PROJECTILE_DAMAGE = 10
CONTACT_DAMAGE = 20

# Level dimensions
PLATFORM_HEIGHT = 20
GROUND_Y = SCREEN_HEIGHT - 50
"""
Level One: Drake vs The Weeknd
"""

from game.levels.level_base import BaseLevel, Platform
from game.settings import *

class LevelOne(BaseLevel):
    """First level: Drake vs The Weeknd"""
    
    def __init__(self):
        super().__init__("Level 1: Drake vs The Weeknd", background_color=(20, 10, 30))
        
        # Custom spawn points for this level
        self.spawn_points = {
            "player": (50, GROUND_Y - 100),
            "enemy": (SCREEN_WIDTH - 100, GROUND_Y - 100)
        }
    
    def create_platforms(self):
        """Create platforms specific to Level One"""
        # Clear existing platforms
        self.platforms.clear()
        
        # Ground
        ground = Platform(0, GROUND_Y, SCREEN_WIDTH, 50, DARK_GRAY)
        self.platforms.append(ground)
        
        # Stage-like platforms for a concert setting
        # Left side platforms (Drake's side)
        left_low = Platform(100, GROUND_Y - 100, 150, PLATFORM_HEIGHT, BLUE)
        left_mid = Platform(50, GROUND_Y - 200, 100, PLATFORM_HEIGHT, BLUE)
        left_high = Platform(150, GROUND_Y - 300, 120, PLATFORM_HEIGHT, BLUE)
        
        # Center platforms
        center_low = Platform(400, GROUND_Y - 80, 200, PLATFORM_HEIGHT, PURPLE)
        center_mid = Platform(450, GROUND_Y - 180, 150, PLATFORM_HEIGHT, PURPLE)
        center_high = Platform(500, GROUND_Y - 280, 100, PLATFORM_HEIGHT, PURPLE)
        
        # Right side platforms (The Weeknd's side)
        right_low = Platform(SCREEN_WIDTH - 250, GROUND_Y - 100, 150, PLATFORM_HEIGHT, PINK)
        right_mid = Platform(SCREEN_WIDTH - 150, GROUND_Y - 200, 100, PLATFORM_HEIGHT, PINK)
        right_high = Platform(SCREEN_WIDTH - 270, GROUND_Y - 300, 120, PLATFORM_HEIGHT, PINK)
        
        # Add all platforms
        self.platforms.extend([
            left_low, left_mid, left_high,
            center_low, center_mid, center_high,
            right_low, right_mid, right_high
        ])
    
    def update(self, dt, player, enemies):
        """Update Level One specific logic"""
        super().update(dt, player, enemies)
        
        # Level-specific update logic can go here
        # For example, special events, time limits, etc.
    
    def render_ui(self, screen):
        """Render Level One specific UI"""
        super().render_ui(screen)
        
        # Add level-specific UI elements
        if not self.completed and not self.failed:
            # Show battle text
            font = pygame.font.Font(None, 32)
            battle_text = font.render("🎵 Musical Battle Royale! 🎵", True, PINK)
            battle_rect = battle_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(battle_text, battle_rect)
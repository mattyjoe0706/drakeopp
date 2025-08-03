"""
Base level class for all game levels
"""

import pygame
from game.settings import *

class Platform:
    """Platform class for level geometry"""
    
    def __init__(self, x, y, width, height, color=GRAY):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
    
    def render(self, screen):
        """Render the platform"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border

class BaseLevel:
    """Base class for all game levels"""
    
    def __init__(self, level_name, background_color=BLACK):
        self.name = level_name
        self.background_color = background_color
        self.platforms = []
        self.spawn_points = {
            "player": (100, GROUND_Y - 100),
            "enemy": (SCREEN_WIDTH - 150, GROUND_Y - 100)
        }
        
        # Level state
        self.completed = False
        self.failed = False
        
        # Create basic level geometry
        self.create_platforms()
    
    def create_platforms(self):
        """Create platforms for this level - override in subclasses"""
        # Default ground platform
        ground = Platform(0, GROUND_Y, SCREEN_WIDTH, 50, DARK_GRAY)
        self.platforms.append(ground)
        
        # Basic platforms
        platform1 = Platform(300, GROUND_Y - 150, 200, PLATFORM_HEIGHT)
        platform2 = Platform(700, GROUND_Y - 250, 200, PLATFORM_HEIGHT)
        platform3 = Platform(200, GROUND_Y - 350, 150, PLATFORM_HEIGHT)
        
        self.platforms.extend([platform1, platform2, platform3])
    
    def get_player_spawn(self):
        """Get player spawn position"""
        return self.spawn_points["player"]
    
    def get_enemy_spawn(self):
        """Get enemy spawn position"""
        return self.spawn_points["enemy"]
    
    def get_platforms(self):
        """Get all platforms in the level"""
        return self.platforms
    
    def update(self, dt, player, enemies):
        """Update level state - override for level-specific logic"""
        # Check win condition (all enemies defeated)
        if all(not enemy.alive for enemy in enemies) and not self.completed:
            self.completed = True
        
        # Check fail condition (player defeated)
        if not player.alive and not self.failed:
            self.failed = True
    
    def render(self, screen):
        """Render the level"""
        # Clear screen with background color
        screen.fill(self.background_color)
        
        # Render platforms
        for platform in self.platforms:
            platform.render(screen)
        
        # Render level info
        self.render_ui(screen)
    
    def render_ui(self, screen):
        """Render level UI elements"""
        # Level name
        font = pygame.font.Font(None, 36)
        level_text = font.render(self.name, True, WHITE)
        screen.blit(level_text, (10, 10))
        
        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Controls: WASD/Arrow Keys to move, SPACE to jump, X to shoot",
            "Defeat all enemies to win!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, WHITE)
            screen.blit(text, (10, 60 + i * 25))
        
        # Game state messages
        if self.completed:
            win_font = pygame.font.Font(None, 72)
            win_text = win_font.render("LEVEL COMPLETE!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_text, win_rect)
        
        elif self.failed:
            fail_font = pygame.font.Font(None, 72)
            fail_text = fail_font.render("GAME OVER", True, RED)
            fail_rect = fail_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(fail_text, fail_rect)
            
            restart_text = instruction_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)
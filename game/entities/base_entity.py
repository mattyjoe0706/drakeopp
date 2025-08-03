"""
Base entity class for all game objects
"""

import pygame
from game.settings import GRAVITY, TERMINAL_VELOCITY, GROUND_Y

class BaseEntity:
    """Base class for all game entities"""
    
    def __init__(self, x, y, width, height, color, name="Entity"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name
        
        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
        # Health
        self.max_health = 100
        self.health = self.max_health
        self.alive = True
        
        # Sprite info
        self.rect = pygame.Rect(x, y, width, height)
        
    def update(self, dt, platforms=None):
        """Update entity physics and position"""
        if not self.alive:
            return
            
        # Apply gravity
        self.vel_y += GRAVITY * dt
        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY
        
        # Update position
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Ground collision
        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Platform collision
        if platforms:
            for platform in platforms:
                if self.check_platform_collision(platform):
                    break
        
        # Keep on screen horizontally
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 1200:  # SCREEN_WIDTH
            self.x = 1200 - self.width
        
        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def check_platform_collision(self, platform):
        """Check and handle collision with a platform"""
        if (self.x < platform.x + platform.width and 
            self.x + self.width > platform.x and
            self.y + self.height >= platform.y and
            self.y + self.height <= platform.y + platform.height + 10 and
            self.vel_y >= 0):
            
            self.y = platform.y - self.height
            self.vel_y = 0
            self.on_ground = True
            return True
        return False
    
    def take_damage(self, damage):
        """Take damage and check if entity dies"""
        if not self.alive:
            return
            
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def render(self, screen):
        """Render the entity"""
        if not self.alive:
            return
            
        # Draw main body
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw name
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 10))
        screen.blit(text, text_rect)
        
        # Draw health bar
        self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen):
        """Draw health bar above entity"""
        bar_width = self.width
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 20
        
        # Background
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
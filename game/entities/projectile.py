"""
Projectile system for bullets and attacks
"""

import pygame
from game.settings import *

class Projectile:
    """Projectile class for bullets and attacks"""
    
    def __init__(self, x, y, direction, projectile_type, owner="neutral"):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.type = projectile_type
        self.owner = owner  # "player", "enemy", or "neutral"
        
        # Visual properties
        self.width = 8
        self.height = 4
        self.color = self.get_color_by_type()
        
        # Physics
        self.velocity = PROJECTILE_SPEED * direction
        self.damage = PROJECTILE_DAMAGE
        
        # State
        self.active = True
        self.lifetime = 3.0  # seconds before auto-destroy
        
        # Collision
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def get_color_by_type(self):
        """Get projectile color based on type"""
        colors = {
            "mic": YELLOW,       # Drake's mic bullets
            "note": PINK,        # The Weeknd's musical notes
            "diamond": CYAN,     # Expensive attacks
            "flame": RED,        # Fire attacks
            "ice": WHITE,        # Ice attacks
        }
        return colors.get(self.type, WHITE)
    
    def update(self, dt):
        """Update projectile position and lifetime"""
        if not self.active:
            return
        
        # Move horizontally
        self.x += self.velocity * dt
        
        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Check bounds
        if self.x < -50 or self.x > SCREEN_WIDTH + 50:
            self.active = False
        
        # Update lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
    
    def check_collision(self, entity):
        """Check collision with an entity"""
        if not self.active or not entity.alive:
            return False
        
        # Don't hit the owner
        if self.owner == "player" and hasattr(entity, 'name') and entity.name == "Drake":
            return False
        if self.owner == "enemy" and hasattr(entity, 'ai'):
            return False
        
        # Check rect collision
        if self.rect.colliderect(entity.rect):
            entity.take_damage(self.damage)
            self.active = False
            return True
        
        return False
    
    def render(self, screen):
        """Render the projectile"""
        if not self.active:
            return
        
        # Draw main projectile
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Add some visual effects based on type
        if self.type == "mic":
            # Add sparkle effect
            pygame.draw.circle(screen, WHITE, self.rect.center, 2)
        elif self.type == "note":
            # Musical note effect
            pygame.draw.circle(screen, WHITE, self.rect.center, 1)
        elif self.type == "flame":
            # Fire trail effect
            trail_rect = pygame.Rect(self.rect.x - 5, self.rect.y, 5, self.height)
            pygame.draw.rect(screen, ORANGE, trail_rect)
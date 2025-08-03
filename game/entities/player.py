"""
Drake - The player character
"""

import pygame
from game.entities.base_entity import BaseEntity
from game.entities.projectile import Projectile
from game.settings import *

class Drake(BaseEntity):
    """Drake - The main player character"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 50, 70, BLUE, "Drake")
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        
        # Player-specific attributes
        self.facing_right = True
        self.shoot_cooldown = 0
        self.shoot_delay = 0.3  # seconds between shots
        
        # Input state
        self.keys_pressed = set()
        
        # Projectiles
        self.projectiles = []
    
    def handle_input(self, keys):
        """Handle player input"""
        self.keys_pressed = set()
        
        # Movement
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
            self.keys_pressed.add('left')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
            self.keys_pressed.add('right')
        
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.keys_pressed.add('jump')
        
        # Shooting
        if keys[pygame.K_x] or keys[pygame.K_j]:
            self.shoot()
            self.keys_pressed.add('shoot')
    
    def shoot(self):
        """Shoot a projectile"""
        if self.shoot_cooldown <= 0:
            # Create projectile
            proj_x = self.x + (self.width if self.facing_right else 0)
            proj_y = self.y + self.height // 2
            direction = 1 if self.facing_right else -1
            
            projectile = Projectile(proj_x, proj_y, direction, "mic", owner="player")
            self.projectiles.append(projectile)
            
            # Reset cooldown
            self.shoot_cooldown = self.shoot_delay
            
            # TODO: Play shoot sound effect
    
    def update(self, dt, platforms=None):
        """Update Drake"""
        super().update(dt, platforms)
        
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            if not projectile.active:
                self.projectiles.remove(projectile)
    
    def get_projectiles(self):
        """Get all active projectiles"""
        return [p for p in self.projectiles if p.active]
    
    def render(self, screen):
        """Render Drake with weapon indicator"""
        if not self.alive:
            return
        
        # Draw main body
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw weapon (mic-bat)
        weapon_color = YELLOW
        if self.facing_right:
            weapon_rect = pygame.Rect(self.rect.right, self.rect.centery - 5, 20, 10)
        else:
            weapon_rect = pygame.Rect(self.rect.left - 20, self.rect.centery - 5, 20, 10)
        pygame.draw.rect(screen, weapon_color, weapon_rect)
        
        # Draw direction indicator
        eye_color = WHITE
        if self.facing_right:
            eye_pos = (self.rect.right - 10, self.rect.top + 15)
        else:
            eye_pos = (self.rect.left + 10, self.rect.top + 15)
        pygame.draw.circle(screen, eye_color, eye_pos, 3)
        
        # Draw name and health bar
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, WHITE)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 10))
        screen.blit(text, text_rect)
        
        self.draw_health_bar(screen)
        
        # Render projectiles
        for projectile in self.projectiles:
            projectile.render(screen)
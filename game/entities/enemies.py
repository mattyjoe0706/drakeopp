"""
Enemy characters and bosses
"""

import pygame
import random
import math
from game.entities.base_entity import BaseEntity
from game.entities.projectile import Projectile
from game.settings import *

class BaseEnemy(BaseEntity):
    """Base class for all enemies"""
    
    def __init__(self, x, y, width, height, color, name):
        super().__init__(x, y, width, height, color, name)
        self.max_health = BOSS_MAX_HEALTH
        self.health = self.max_health
        
        # AI properties
        self.ai_timer = 0
        self.action_cooldown = 0
        self.facing_right = False
        
        # Projectiles
        self.projectiles = []
        
        # Target (usually the player)
        self.target = None
    
    def set_target(self, target):
        """Set the target for AI"""
        self.target = target
    
    def update(self, dt, platforms=None):
        """Update enemy AI and physics"""
        super().update(dt, platforms)
        
        if not self.alive or not self.target:
            return
        
        # Update AI
        self.update_ai(dt)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            if not projectile.active:
                self.projectiles.remove(projectile)
    
    def update_ai(self, dt):
        """Override in subclasses for specific AI behavior"""
        pass
    
    def get_projectiles(self):
        """Get all active projectiles"""
        return [p for p in self.projectiles if p.active]
    
    def shoot_at_target(self, projectile_type="note"):
        """Shoot a projectile towards the target"""
        if not self.target or not self.alive:
            return
        
        # Calculate direction to target
        target_center_x = self.target.x + self.target.width / 2
        self_center_x = self.x + self.width / 2
        
        direction = 1 if target_center_x > self_center_x else -1
        self.facing_right = direction > 0
        
        # Create projectile
        proj_x = self.x + (self.width if self.facing_right else 0)
        proj_y = self.y + self.height // 2
        
        projectile = Projectile(proj_x, proj_y, direction, projectile_type, owner="enemy")
        self.projectiles.append(projectile)
    
    def render(self, screen):
        """Render enemy with direction indicator"""
        if not self.alive:
            return
        
        # Draw main body
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw direction indicator (simple eye)
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


class TheWeeknd(BaseEnemy):
    """The Weeknd - First boss enemy"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 60, 80, PINK, "The Weeknd")
        
        # The Weeknd specific attributes
        self.attack_patterns = ["single_shot", "triple_shot", "wave_shot"]
        self.current_pattern = 0
        self.pattern_timer = 0
        self.move_timer = 0
        self.move_direction = 1
        
        # AI timing
        self.ai_update_interval = 0.1  # Update AI every 100ms
        self.attack_interval = 2.0     # Attack every 2 seconds
    
    def update_ai(self, dt):
        """The Weeknd's AI behavior"""
        self.ai_timer += dt
        self.pattern_timer += dt
        self.move_timer += dt
        self.action_cooldown -= dt
        
        # Simple movement AI
        if self.move_timer >= 1.5:  # Change direction every 1.5 seconds
            self.move_direction *= -1
            self.move_timer = 0
        
        # Move horizontally
        self.vel_x = 50 * self.move_direction
        
        # Attack patterns
        if self.action_cooldown <= 0:
            self.execute_attack_pattern()
            self.action_cooldown = self.attack_interval
            
            # Change pattern occasionally
            if random.random() < 0.3:
                self.current_pattern = (self.current_pattern + 1) % len(self.attack_patterns)
    
    def execute_attack_pattern(self):
        """Execute current attack pattern"""
        pattern = self.attack_patterns[self.current_pattern]
        
        if pattern == "single_shot":
            self.shoot_at_target("note")
        
        elif pattern == "triple_shot":
            # Shoot three projectiles in quick succession
            for i in range(3):
                # Slightly offset timing for visual effect
                if i == 0:
                    self.shoot_at_target("note")
        
        elif pattern == "wave_shot":
            # Shoot projectiles in different directions
            for direction in [-1, 0, 1]:
                proj_x = self.x + self.width // 2
                proj_y = self.y + self.height // 2
                
                # Create projectile with slight angle variation
                if direction == 0:
                    self.shoot_at_target("note")
                else:
                    projectile = Projectile(proj_x, proj_y, direction, "note", owner="enemy")
                    self.projectiles.append(projectile)
    
    def render(self, screen):
        """Render The Weeknd with special effects"""
        super().render(screen)
        
        if not self.alive:
            return
        
        # Add musical notes floating around (visual effect)
        if random.random() < 0.1:  # 10% chance each frame
            note_x = self.rect.x + random.randint(-20, self.width + 20)
            note_y = self.rect.y + random.randint(-10, self.height + 10)
            pygame.draw.circle(screen, PINK, (int(note_x), int(note_y)), 2)


class Future(BaseEnemy):
    """Future - Fast moving enemy with rapid fire"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 50, 75, PURPLE, "Future")
        self.attack_interval = 1.0  # Faster attacks
        self.move_speed = 80
    
    def update_ai(self, dt):
        """Future's fast-paced AI"""
        self.ai_timer += dt
        self.action_cooldown -= dt
        
        # Quick movement towards/away from player
        if self.target:
            distance = abs(self.target.x - self.x)
            if distance > 200:
                # Move towards player
                direction = 1 if self.target.x > self.x else -1
                self.vel_x = self.move_speed * direction
            else:
                # Move away from player (hit and run)
                direction = -1 if self.target.x > self.x else 1
                self.vel_x = self.move_speed * direction
        
        # Rapid fire attacks
        if self.action_cooldown <= 0:
            self.shoot_at_target("diamond")
            self.action_cooldown = self.attack_interval


# Additional enemies can be added here following the same pattern
class RickRoss(BaseEnemy):
    """Rick Ross - Tank enemy with powerful but slow attacks"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 80, 90, ORANGE, "Rick Ross")
        self.max_health = BOSS_MAX_HEALTH * 1.5  # More health
        self.health = self.max_health
        self.attack_interval = 3.0  # Slower but more powerful
    
    def update_ai(self, dt):
        """Rick Ross's tank-like AI"""
        self.action_cooldown -= dt
        
        # Slow movement
        if self.target:
            direction = 1 if self.target.x > self.x else -1
            self.vel_x = 30 * direction  # Slower movement
        
        # Powerful attacks
        if self.action_cooldown <= 0:
            # Double shot
            self.shoot_at_target("flame")
            # Second shot with slight delay would be handled in a more complex system
            self.action_cooldown = self.attack_interval
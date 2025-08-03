"""
Main game manager that coordinates all game systems
"""

import pygame
from game.entities.player import Drake
from game.entities.enemies import TheWeeknd
from game.levels.level_one import LevelOne
from game.audio.sound_manager import sound_manager
from game.settings import *

class GameManager:
    """Main game manager class"""
    
    def __init__(self, screen):
        self.screen = screen
        
        # Game state
        self.game_state = "playing"  # "playing", "paused", "game_over", "level_complete"
        self.current_level = None
        
        # Entities
        self.player = None
        self.enemies = []
        
        # Initialize first level
        self.start_level_one()
        
        # Start background music
        sound_manager.play_music("bg_music_level1")
    
    def start_level_one(self):
        """Initialize Level One"""
        self.current_level = LevelOne()
        
        # Create player
        player_spawn = self.current_level.get_player_spawn()
        self.player = Drake(player_spawn[0], player_spawn[1])
        
        # Create enemies
        self.enemies.clear()
        enemy_spawn = self.current_level.get_enemy_spawn()
        weeknd = TheWeeknd(enemy_spawn[0], enemy_spawn[1])
        weeknd.set_target(self.player)
        self.enemies.append(weeknd)
    
    def restart_level(self):
        """Restart the current level"""
        if isinstance(self.current_level, LevelOne):
            self.start_level_one()
        self.game_state = "playing"
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart level
                if self.game_state in ["game_over", "level_complete"]:
                    self.restart_level()
            elif event.key == pygame.K_p:
                # Pause/unpause
                if self.game_state == "playing":
                    self.game_state = "paused"
                elif self.game_state == "paused":
                    self.game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                # Quit game
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def update(self, dt):
        """Update all game systems"""
        if self.game_state != "playing":
            return
        
        # Handle player input
        keys = pygame.key.get_pressed()
        if self.player and self.player.alive:
            self.player.handle_input(keys)
        
        # Update entities
        platforms = self.current_level.get_platforms()
        
        if self.player:
            self.player.update(dt, platforms)
        
        for enemy in self.enemies:
            enemy.update(dt, platforms)
        
        # Handle projectile collisions
        self.handle_collisions()
        
        # Update level
        self.current_level.update(dt, self.player, self.enemies)
        
        # Check game state changes
        if self.current_level.completed and self.game_state == "playing":
            self.game_state = "level_complete"
            sound_manager.play_sound("level_complete")
        elif self.current_level.failed and self.game_state == "playing":
            self.game_state = "game_over"
            sound_manager.play_sound("game_over")
    
    def handle_collisions(self):
        """Handle all collision detection"""
        if not self.player or not self.player.alive:
            return
        
        # Player projectiles vs enemies
        for projectile in self.player.get_projectiles():
            for enemy in self.enemies:
                if projectile.check_collision(enemy):
                    sound_manager.play_sound("enemy_hit")
                    break
        
        # Enemy projectiles vs player
        for enemy in self.enemies:
            for projectile in enemy.get_projectiles():
                if projectile.check_collision(self.player):
                    sound_manager.play_sound("player_hit")
                    break
        
        # Direct entity collision (contact damage)
        for enemy in self.enemies:
            if (enemy.alive and self.player.alive and 
                enemy.rect.colliderect(self.player.rect)):
                
                # Apply contact damage
                self.player.take_damage(CONTACT_DAMAGE)
                enemy.take_damage(CONTACT_DAMAGE)
                sound_manager.play_sound("player_hit")
                
                # Push entities apart to prevent continuous damage
                if enemy.x < self.player.x:
                    enemy.x -= 20
                    self.player.x += 20
                else:
                    enemy.x += 20
                    self.player.x -= 20
    
    def render(self):
        """Render all game elements"""
        # Render level (includes background and platforms)
        self.current_level.render(self.screen)
        
        # Render entities
        if self.player:
            self.player.render(self.screen)
        
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        # Render UI overlay
        self.render_ui()
    
    def render_ui(self):
        """Render UI overlay"""
        # Game state messages
        if self.game_state == "paused":
            self.render_pause_screen()
        elif self.game_state == "game_over":
            self.render_game_over_screen()
        elif self.game_state == "level_complete":
            self.render_level_complete_screen()
        
        # Always show FPS (debug info)
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {int(pygame.time.Clock().get_fps())}", True, WHITE)
        self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
    
    def render_pause_screen(self):
        """Render pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.Font(None, 72)
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 32)
        instruction_text = instruction_font.render("Press P to resume", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instruction_text, instruction_rect)
    
    def render_game_over_screen(self):
        """Render game over screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 32)
        restart_text = instruction_font.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
        
        quit_text = instruction_font.render("Press ESC to quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(quit_text, quit_rect)
    
    def render_level_complete_screen(self):
        """Render level complete screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Level complete text
        font = pygame.font.Font(None, 72)
        complete_text = font.render("LEVEL COMPLETE!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(complete_text, complete_rect)
        
        # Victory message
        message_font = pygame.font.Font(None, 32)
        victory_text = message_font.render("Drake defeats The Weeknd!", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(victory_text, victory_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        restart_text = instruction_font.render("Press R to play again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
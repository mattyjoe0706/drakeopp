#!/usr/bin/env python3
"""
Drake vs The Opps - 2D Action Platformer
Main game entry point
"""

import pygame
import sys
from game.game_manager import GameManager
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE

def main():
    """Initialize and run the game"""
    pygame.init()
    pygame.mixer.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    # Create game manager
    game_manager = GameManager(screen)
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)
        
        # Update game
        game_manager.update(dt)
        
        # Render game
        game_manager.render()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
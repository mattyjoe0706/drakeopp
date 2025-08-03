"""
Sound manager for game audio
"""

import pygame

class SoundManager:
    """Manages all game audio and sound effects"""
    
    def __init__(self):
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Sound effect placeholders
        self.sounds = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        
        # Initialize placeholder sounds
        self.init_placeholder_sounds()
    
    def init_placeholder_sounds(self):
        """Initialize placeholder sound effects"""
        # For now, we'll create simple tone-based sound effects
        # In a full game, these would be loaded from audio files
        
        self.sounds = {
            "player_shoot": None,
            "enemy_shoot": None,
            "player_hit": None,
            "enemy_hit": None,
            "player_jump": None,
            "level_complete": None,
            "game_over": None,
            "bg_music_level1": None
        }
        
        # TODO: Load actual sound files when available
        # Example:
        # self.sounds["player_shoot"] = pygame.mixer.Sound("sounds/player_shoot.wav")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(self.sfx_volume)
                sound.play()
            except pygame.error:
                print(f"Could not play sound: {sound_name}")
        else:
            # Placeholder: Print sound effect name
            print(f"♪ {sound_name.upper()} ♪")
    
    def play_music(self, music_name, loop=-1):
        """Play background music"""
        if music_name in self.sounds and self.sounds[music_name]:
            try:
                pygame.mixer.music.load(self.sounds[music_name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loop)
            except pygame.error:
                print(f"Could not play music: {music_name}")
        else:
            # Placeholder: Print music name
            print(f"🎵 Now playing: {music_name} 🎵")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def load_sound(self, sound_name, file_path):
        """Load a sound file"""
        try:
            self.sounds[sound_name] = pygame.mixer.Sound(file_path)
            print(f"Loaded sound: {sound_name}")
        except pygame.error as e:
            print(f"Could not load sound {sound_name}: {e}")
    
    def load_music(self, music_name, file_path):
        """Load a music file"""
        # For music, we store the file path since pygame.mixer.music loads files directly
        self.sounds[music_name] = file_path
        print(f"Loaded music: {music_name}")

# Global sound manager instance
sound_manager = SoundManager()
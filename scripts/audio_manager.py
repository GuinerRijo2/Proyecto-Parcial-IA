"""
Sistema de manejo de audio para Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import os
from .settings import *

class AudioManager:
    """Clase para manejar música y efectos de sonido"""
    
    def __init__(self):
        # Initialize mixer with specific settings for compatibility
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        
        # Get mixer settings for audio generation
        self.mixer_frequency = pygame.mixer.get_init()[0]
        self.mixer_size = pygame.mixer.get_init()[1]
        self.mixer_channels = pygame.mixer.get_init()[2]
        
        # Configurar volúmenes
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        
        # Cargar sonidos básicos (crearemos archivos temporales si no existen)
        self.load_default_sounds()
    
    def load_default_sounds(self):
        """Cargar sonidos por defecto o crear placeholders"""
        sound_files = {
            "shoot": "assets/sounds/shoot.mp3",
            "alien_death": "assets/sounds/alien_death.mp3",
            "player_hit": "assets/sounds/player_hit.mp3",
            "menu_move": "assets/sounds/menu_move.mp3",
            "menu_select": "assets/sounds/menu_select.mp3",
            "powerup": "assets/sounds/powerup.mp3"
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    sound = pygame.mixer.Sound(file_path)
                    sound.set_volume(SOUND_VOLUME)
                    self.sounds[sound_name] = sound
                else:
                    # Crear sonido sintético básico como placeholder
                    self.sounds[sound_name] = self.create_synthetic_sound(sound_name)
            except Exception as e:
                print(f"Error cargando sonido {sound_name}: {e}")
                self.sounds[sound_name] = self.create_synthetic_sound(sound_name)
    
    def create_synthetic_sound(self, sound_type):
        """Crear sonidos sintéticos básicos"""
        try:
            import numpy as np
            
            # Use mixer settings
            sample_rate = self.mixer_frequency or 22050
            duration = 0.2
            
            if sound_type == "shoot":
                # Sonido de disparo: ruido blanco corto
                samples = np.random.normal(0, 0.3, int(sample_rate * 0.1))
                # Envelope de decaimiento
                envelope = np.exp(-np.linspace(0, 10, len(samples)))
                samples = samples * envelope
            elif sound_type == "alien_death":
                # Sonido de muerte: sweep descendente
                t = np.linspace(0, duration, int(sample_rate * duration))
                freq = 800 * np.exp(-t * 5)
                samples = 0.3 * np.sin(2 * np.pi * freq * t)
            elif sound_type in ["menu_move", "menu_select"]:
                # Sonidos de menú: tonos simples
                freq = 800 if sound_type == "menu_move" else 1200
                t = np.linspace(0, 0.1, int(sample_rate * 0.1))
                samples = 0.2 * np.sin(2 * np.pi * freq * t)
            else:
                # Sonido genérico
                t = np.linspace(0, 0.1, int(sample_rate * 0.1))
                samples = 0.1 * np.sin(2 * np.pi * 440 * t)
            
            # Convertir a formato pygame según la configuración del mixer
            samples = (samples * 32767).astype(np.int16)
            
            # Asegurar que el número de canales coincida con el mixer
            if self.mixer_channels == 2:
                # Stereo: duplicar para crear dos canales
                if len(samples.shape) == 1:
                    samples = np.column_stack((samples, samples))
            else:
                # Mono: asegurar que sea 1D
                if len(samples.shape) > 1:
                    samples = samples.flatten()
            
            sound = pygame.sndarray.make_sound(samples)
            sound.set_volume(SOUND_VOLUME)
            return sound
            
        except Exception as e:
            print(f"Error creando sonido sintético {sound_type}: {e}")
            # Crear sonido silencioso como fallback
            return self.create_silent_sound()
    
    def create_silent_sound(self):
        """Crear un sonido silencioso como fallback"""
        try:
            import numpy as np
            sample_rate = self.mixer_frequency or 22050
            samples = np.zeros(int(sample_rate * 0.1), dtype=np.int16)
            
            if self.mixer_channels == 2:
                samples = np.column_stack((samples, samples))
                
            return pygame.sndarray.make_sound(samples)
        except:
            # Si todo falla, usar pygame.mixer.Sound con datos mínimos
            return pygame.mixer.Sound(buffer=b'\x00\x00' * 100)
    
    def load_music(self, file_path):
        """Cargar música de fondo"""
        try:
            if os.path.exists(file_path):
                pygame.mixer.music.load(file_path)
                return True
            else:
                print(f"Archivo de música no encontrado: {file_path}")
                return False
        except Exception as e:
            print(f"Error cargando música: {e}")
            return False
    
    def play_music(self, loops=-1):
        """Reproducir música de fondo"""
        try:
            pygame.mixer.music.play(loops)
            self.music_playing = True
        except Exception as e:
            print(f"Error reproduciendo música: {e}")
    
    def stop_music(self):
        """Detener música de fondo"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def play_sound(self, sound_name):
        """Reproducir efecto de sonido"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sonido no encontrado: {sound_name}")
    
    def set_music_volume(self, volume):
        """Ajustar volumen de la música"""
        pygame.mixer.music.set_volume(max(0, min(1, volume)))
    
    def set_sound_volume(self, volume):
        """Ajustar volumen de los efectos"""
        for sound in self.sounds.values():
            sound.set_volume(max(0, min(1, volume))) 
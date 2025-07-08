"""
Configuración y constantes del juego Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame

# Configuración de pantalla
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Configuración del juego
TILE_SIZE = 32
PLAYER_SPEED = 200
PLAYER_HEALTH = 100
PLAYER_AMMO = 100
BULLET_SPEED = 400
ALIEN_SPEED = 80
ALIEN_HEALTH = 50
BULLET_DAMAGE = 25
ALIEN_BULLET_DAMAGE = 15

# Estados del juego
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_PAUSED = "paused"

# Teclas de control
KEY_UP = pygame.K_w
KEY_DOWN = pygame.K_s
KEY_LEFT = pygame.K_a
KEY_RIGHT = pygame.K_d
KEY_SHOOT = pygame.K_SPACE
KEY_PAUSE = pygame.K_ESCAPE
KEY_ENTER = pygame.K_RETURN

# Configuración de audio
MUSIC_VOLUME = 0.7
SOUND_VOLUME = 0.8

# Configuración de IA
AI_UPDATE_INTERVAL = 0.1  # Actualizar IA cada 100ms
PATHFINDING_UPDATE_INTERVAL = 0.5  # Recalcular rutas cada 500ms
VISION_RANGE = 200  # Rango de visión de los aliens
ATTACK_RANGE = 100   # Rango de ataque de los aliens

# Configuración del mapa
MAP_WIDTH = 40
MAP_HEIGHT = 30
WALL_TILE = 1
FLOOR_TILE = 0

# Audio
AUDIO_FREQUENCY = 22050
AUDIO_SIZE = -16
AUDIO_CHANNELS = 2
AUDIO_BUFFER = 1024

# Debug
DEBUG = True  # Temporalmente habilitado para diagnosticar colisiones 
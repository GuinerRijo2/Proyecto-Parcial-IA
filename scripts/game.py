"""
Clase principal del juego Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import sys
from .settings import *
from .menu import Menu
from .level import Level
from .input_handler import InputHandler
from .audio_manager import AudioManager

class Game:
    """Clase principal que maneja los estados del juego"""
    
    def __init__(self, screen):
        self.screen = screen
        self.state = GAME_STATE_MENU
        self.clock = pygame.time.Clock()
        
        # Inicializar sistemas
        self.input_handler = InputHandler()
        self.audio_manager = AudioManager()
        
        # Inicializar estados
        self.menu = Menu(self)
        self.level = None
        
        # Cargar recursos
        self.load_resources()
        
        print("Alien Breed 92 SE iniciado")
    
    def load_resources(self):
        """Cargar recursos del juego"""
        try:
            # La música y sonidos se cargarán desde AudioManager
            self.audio_manager.load_music("assets/music/main_theme.ogg")
            self.audio_manager.play_music()
        except Exception as e:
            print(f"Error cargando recursos: {e}")
    
    def handle_event(self, event):
        """Manejar eventos según el estado actual"""
        self.input_handler.handle_event(event)
        
        if self.state == GAME_STATE_MENU:
            self.menu.handle_event(event)
        elif self.state == GAME_STATE_PLAYING:
            if self.level:
                self.level.handle_event(event)
        elif self.state == GAME_STATE_PAUSED:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_PAUSE:
                    self.state = GAME_STATE_PLAYING
    
    def update(self, dt):
        """Actualizar lógica del juego según el estado actual"""
        # Actualizar input handler cada frame
        self.input_handler.update()
        
        if self.state == GAME_STATE_MENU:
            self.menu.update()  # Menú no necesita dt
        elif self.state == GAME_STATE_PLAYING:
            if self.level:
                self.level.update(dt)
                # Verificar si el juego ha terminado
                if self.level.game_over:
                    self.state = GAME_STATE_GAME_OVER
        elif self.state == GAME_STATE_GAME_OVER:
            # Manejar estado de game over
            pass
    
    def draw(self):
        """Renderizar según el estado actual"""
        self.screen.fill(BLACK)
        
        if self.state == GAME_STATE_MENU:
            self.menu.draw(self.screen)
        elif self.state == GAME_STATE_PLAYING:
            if self.level:
                self.level.draw(self.screen)
        elif self.state == GAME_STATE_PAUSED:
            if self.level:
                self.level.draw(self.screen)
            self.draw_pause_overlay()
        elif self.state == GAME_STATE_GAME_OVER:
            self.draw_game_over_screen()
    
    def draw_pause_overlay(self):
        """Dibujar overlay de pausa"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
    
    def draw_game_over_screen(self):
        """Dibujar pantalla de game over"""
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        text_restart = font_small.render("Press ESC to return to menu", True, WHITE)
        text_restart_rect = text_restart.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(text_restart, text_restart_rect)
    
    def start_game(self):
        """Iniciar una nueva partida"""
        self.level = Level(self)
        self.state = GAME_STATE_PLAYING
        print("Nueva partida iniciada")
    
    def return_to_menu(self):
        """Volver al menú principal"""
        self.level = None
        self.state = GAME_STATE_MENU
    
    def quit_game(self):
        """Salir del juego"""
        pygame.quit()
        sys.exit() 
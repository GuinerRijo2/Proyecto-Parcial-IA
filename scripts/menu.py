"""
Sistema de menú del juego Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
from .settings import *

class Menu:
    """Clase para manejar el menú principal del juego"""
    
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Jugar", "Salir"]
        self.font = pygame.font.Font(None, 74)
        self.title_font = pygame.font.Font(None, 96)
        
        # Para evitar navegación muy rápida
        self.last_input_time = 0
        self.input_delay = 200  # milisegundos
        
        # Colores del menú
        self.title_color = GREEN
        self.selected_color = YELLOW
        self.normal_color = WHITE
        
        # Animación del título
        self.title_pulse = 0
        self.pulse_speed = 2
    
    def handle_event(self, event):
        """Manejar eventos del menú"""
        current_time = pygame.time.get_ticks()
        
        if event.type == pygame.KEYDOWN:
            if current_time - self.last_input_time > self.input_delay:
                if event.key == KEY_UP or event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    self.last_input_time = current_time
                elif event.key == KEY_DOWN or event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    self.last_input_time = current_time
                elif event.key == KEY_ENTER or event.key == KEY_SHOOT:
                    self.select_option()
        
        # Manejar entrada de gamepad usando el input_handler
        input_handler = self.game.input_handler
        input_handler.handle_event(event)  # Procesar eventos del gamepad
        
    def update(self):
        """Actualizar menú (para navegación con gamepad)"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_input_time > self.input_delay:
            input_handler = self.game.input_handler
            input_handler.update()  # Actualizar estados
            
            move_x, move_y = input_handler.get_movement_vector()
            
            # Navegación con gamepad
            if move_y < -0.5:  # Arriba
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.last_input_time = current_time
            elif move_y > 0.5:  # Abajo
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.last_input_time = current_time
                
            # Selección con gamepad
            if input_handler.is_shooting():
                self.select_option()
            
    def select_option(self):
        """Seleccionar opción del menú"""
        if self.selected_option == 0:  # Jugar
            self.game.start_game()
        elif self.selected_option == 1:  # Salir
            self.game.quit_game()
    
    def update_animation(self, dt):
        """Actualizar animaciones del menú"""
        self.title_pulse += self.pulse_speed * dt
        if self.title_pulse > 1:
            self.title_pulse = 1
            self.pulse_speed = -2
        elif self.title_pulse < 0:
            self.title_pulse = 0
            self.pulse_speed = 2
    
    def draw(self, screen):
        """Dibujar el menú"""
        # Fondo
        screen.fill(BLACK)
        
        # Título
        title_text = self.title_font.render("ALIEN BREED 92 SE", True, self.title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.font.render("Clone Pygame Edition", True, self.normal_color)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.normal_color
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 80))
            screen.blit(option_text, option_rect)
            
        # Indicador de selección
        arrow_text = self.font.render(">", True, self.selected_color)
        arrow_rect = arrow_text.get_rect(center=(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + self.selected_option * 80))
        screen.blit(arrow_text, arrow_rect)
        
        # Información de controles
        instructions = [
            "=== CONTROLES ===",
            "",
            "TECLADO:",
            "  WASD o Flechas - Movimiento",
            "  ESPACIO - Disparar",
            "  ESC - Pausa/Menú",
            "",
            "GAMEPAD:",
            "  Stick izq. o D-pad - Movimiento", 
            "  X (PS) / A (Xbox) - Disparar",
            "  Options (PS) / Menu (Xbox) - Pausa",
            "",
            "Ambos controles funcionan simultáneamente"
        ]
        
        # Mostrar información de entrada actual
        input_handler = self.game.input_handler
        if hasattr(input_handler, 'gamepad') and input_handler.gamepad:
            gamepad_name = input_handler.gamepad.get_name()
            if "DualSense" in gamepad_name:
                gamepad_info = "Mando PS5 DualSense conectado"
            elif "Xbox" in gamepad_name:
                gamepad_info = "Mando Xbox conectado"
            else:
                gamepad_info = f"Gamepad conectado: {gamepad_name}"
        else:
            gamepad_info = "Solo teclado disponible"
            
        instructions.append("")
        instructions.append(f"Estado: {gamepad_info}")
        
        for i, instruction in enumerate(instructions):
            if instruction == "=== CONTROLES ===":
                inst_font = pygame.font.Font(None, 32)
                color = YELLOW
            elif instruction.startswith("TECLADO:") or instruction.startswith("GAMEPAD:"):
                inst_font = pygame.font.Font(None, 28)
                color = GREEN
            elif instruction.startswith("Estado:"):
                inst_font = pygame.font.Font(None, 24)
                color = BLUE
            else:
                inst_font = pygame.font.Font(None, 24)
                color = GRAY
                
            if instruction.strip():  # No dibujar líneas vacías
                inst_text = inst_font.render(instruction, True, color)
                inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 320 + i * 20))
                screen.blit(inst_text, inst_rect) 
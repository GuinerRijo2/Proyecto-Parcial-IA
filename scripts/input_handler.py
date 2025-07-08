"""
Sistema de manejo de entrada para Alien Breed 92 SE
Soporta tanto teclado como gamepad simultáneamente
"""

import pygame
import math
from .settings import *

class InputHandler:
    """Clase para manejar entrada de teclado y gamepad"""
    
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.gamepad = None
        self.init_gamepad()
        
        # Estados de entrada combinados
        self.move_x = 0
        self.move_y = 0
        self.shooting = False
        self.pause_pressed = False
        
        # Estados por separado para depuración
        self.keyboard_move_x = 0
        self.keyboard_move_y = 0
        self.keyboard_shooting = False
        
        self.gamepad_move_x = 0
        self.gamepad_move_y = 0
        self.gamepad_shooting = False
        
    def init_gamepad(self):
        """Inicializar gamepad si está disponible"""
        try:
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.gamepad = pygame.joystick.Joystick(0)
                self.gamepad.init()
                gamepad_name = self.gamepad.get_name()
                print(f"Gamepad conectado: {gamepad_name}")
                
                # Mostrar información específica del mando
                if "DualSense" in gamepad_name:
                    print("  - Mando PS5 DualSense detectado")
                    print("  - Usar stick izquierdo o D-pad para moverse")
                    print("  - Botón X (Cruz) para disparar")
                    print("  - Botón Options para pausa")
                elif "Xbox" in gamepad_name:
                    print("  - Mando Xbox detectado")
                    print("  - Usar stick izquierdo o D-pad para moverse")
                    print("  - Botón A para disparar")
                    print("  - Botón Menu para pausa")
                else:
                    print("  - Mando genérico detectado")
            else:
                print("No hay gamepad conectado - usando solo teclado")
        except Exception as e:
            print(f"Error inicializando gamepad: {e}")
            self.gamepad = None
    
    def handle_event(self, event):
        """Manejar eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_PAUSE:
                self.pause_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == KEY_PAUSE:
                self.pause_pressed = False
        
        # Manejar eventos de gamepad
        if event.type == pygame.JOYBUTTONDOWN and self.gamepad and event.joy == 0:
            self._handle_gamepad_button_down(event.button)
        elif event.type == pygame.JOYBUTTONUP and self.gamepad and event.joy == 0:
            self._handle_gamepad_button_up(event.button)
            
    def _handle_gamepad_button_down(self, button):
        """Manejar botones presionados del gamepad"""
        if not self.gamepad:
            return
            
        gamepad_name = self.gamepad.get_name()
        
        if "DualSense" in gamepad_name:
            # Mapeo para PS5 DualSense
            if button == 0:  # Botón X (Cruz)
                self.gamepad_shooting = True
            elif button == 9:  # Botón Options
                self.pause_pressed = True
        else:
            # Mapeo para Xbox y otros mandos
            if button == 0:  # Botón A (Xbox) / X (PlayStation genérico)
                self.gamepad_shooting = True
            elif button == 7:  # Botón Start/Menu
                self.pause_pressed = True
                
    def _handle_gamepad_button_up(self, button):
        """Manejar botones soltados del gamepad"""
        if not self.gamepad:
            return
            
        gamepad_name = self.gamepad.get_name()
        
        if "DualSense" in gamepad_name:
            # Mapeo para PS5 DualSense
            if button == 0:  # Botón X (Cruz)
                self.gamepad_shooting = False
            elif button == 9:  # Botón Options
                self.pause_pressed = False
        else:
            # Mapeo para Xbox y otros mandos
            if button == 0:  # Botón A (Xbox) / X (PlayStation genérico)
                self.gamepad_shooting = False
            elif button == 7:  # Botón Start/Menu
                self.pause_pressed = False
    
    def update(self):
        """Actualizar estados de entrada"""
        # Verificar si el gamepad se desconectó
        if self.gamepad:
            try:
                # Intentar acceder al gamepad para verificar que esté conectado
                self.gamepad.get_numaxes()
            except:
                print("Gamepad desconectado, intentando reconectar...")
                self.init_gamepad()
        
        # Actualizar teclas
        self.keys = pygame.key.get_pressed()
        
        # ===== ENTRADA DE TECLADO =====
        self.keyboard_move_x = 0
        self.keyboard_move_y = 0
        
        # Movimiento con WASD
        if self.keys[KEY_LEFT]:  # A
            self.keyboard_move_x -= 1
        if self.keys[KEY_RIGHT]:  # D
            self.keyboard_move_x += 1
        if self.keys[KEY_UP]:  # W
            self.keyboard_move_y -= 1
        if self.keys[KEY_DOWN]:  # S
            self.keyboard_move_y += 1
        
        # También soportar flechas
        if self.keys[pygame.K_LEFT]:
            self.keyboard_move_x -= 1
        if self.keys[pygame.K_RIGHT]:
            self.keyboard_move_x += 1
        if self.keys[pygame.K_UP]:
            self.keyboard_move_y -= 1
        if self.keys[pygame.K_DOWN]:
            self.keyboard_move_y += 1
        
        # Disparo con teclado
        self.keyboard_shooting = self.keys[KEY_SHOOT]
        
        # ===== ENTRADA DE GAMEPAD =====
        self.gamepad_move_x = 0
        self.gamepad_move_y = 0
        
        if self.gamepad:
            try:
                # Stick analógico izquierdo
                axis_x = self.gamepad.get_axis(0)
                axis_y = self.gamepad.get_axis(1)
                
                # Zona muerta
                deadzone = 0.12
                if abs(axis_x) > deadzone:
                    self.gamepad_move_x = axis_x
                if abs(axis_y) > deadzone:
                    self.gamepad_move_y = axis_y
                
                # D-pad como respaldo (solo si el stick no está siendo usado)
                if abs(self.gamepad_move_x) < deadzone and abs(self.gamepad_move_y) < deadzone:
                    gamepad_name = self.gamepad.get_name()
                    
                    if "DualSense" in gamepad_name:
                        # PS5 DualSense - d-pad son botones individuales
                        if self.gamepad.get_button(11):  # D-pad izquierda
                            self.gamepad_move_x = -1
                        elif self.gamepad.get_button(15) or self.gamepad.get_button(14):  # D-pad derecha
                            self.gamepad_move_x = 1
                            
                        if self.gamepad.get_button(12):  # D-pad arriba
                            self.gamepad_move_y = -1
                        elif self.gamepad.get_button(13):  # D-pad abajo
                            self.gamepad_move_y = 1
                    else:
                        # Otros mandos que usan hat
                        if self.gamepad.get_numhats() > 0:
                            hat = self.gamepad.get_hat(0)
                            if hat[0] != 0:
                                self.gamepad_move_x = hat[0]
                            if hat[1] != 0:
                                self.gamepad_move_y = -hat[1]  # Invertir Y
                                
            except Exception as e:
                print(f"Error leyendo gamepad: {e}")
                self.gamepad_move_x = 0
                self.gamepad_move_y = 0
                # Intentar reconectar gamepad en caso de error
                self.init_gamepad()
        
        # ===== COMBINAR ENTRADAS =====
        # Combinar ambas entradas en lugar de priorizar una sobre otra
        combined_x = self.keyboard_move_x + self.gamepad_move_x
        combined_y = self.keyboard_move_y + self.gamepad_move_y
        
        # Limitar a -1, 1 para evitar movimiento demasiado rápido
        self.move_x = max(-1, min(1, combined_x))
        self.move_y = max(-1, min(1, combined_y))
        
        # Normalizar movimiento diagonal si es necesario
        if abs(self.move_x) > 0.1 and abs(self.move_y) > 0.1:
            length = math.sqrt(self.move_x * self.move_x + self.move_y * self.move_y)
            if length > 1:
                self.move_x /= length
                self.move_y /= length
        
        # Combinar disparo (cualquiera de los dos)
        self.shooting = self.keyboard_shooting or self.gamepad_shooting
    
    def get_movement_vector(self):
        """Obtener vector de movimiento normalizado"""
        return self.move_x, self.move_y
    
    def is_shooting(self):
        """Verificar si se está disparando"""
        return self.shooting
    
    def is_pause_pressed(self):
        """Verificar si se presionó pausa"""
        return self.pause_pressed
        
    def get_input_info(self):
        """Obtener información de entrada para depuración"""
        return {
            'keyboard': {
                'move': (self.keyboard_move_x, self.keyboard_move_y),
                'shoot': self.keyboard_shooting
            },
            'gamepad': {
                'move': (self.gamepad_move_x, self.gamepad_move_y),
                'shoot': self.gamepad_shooting,
                'connected': self.gamepad is not None
            },
            'combined': {
                'move': (self.move_x, self.move_y),
                'shoot': self.shooting
            }
        } 
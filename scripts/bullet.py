"""
Clase para las balas en Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import math
from .settings import *

class Bullet:
    """Clase que representa una bala"""
    
    def __init__(self, x, y, angle, owner, sprite_manager):
        self.x = x
        self.y = y
        self.angle = angle
        self.owner = owner  # "player" o "alien"
        self.sprite_manager = sprite_manager
        
        # Velocidad
        self.speed = BULLET_SPEED
        angle_rad = math.radians(angle)
        self.vel_x = math.cos(angle_rad) * self.speed
        self.vel_y = math.sin(angle_rad) * self.speed
        
        # Propiedades
        self.damage = BULLET_DAMAGE if owner == "player" else ALIEN_BULLET_DAMAGE
        self.lifetime = 3000  # 3 segundos
        self.age = 0
        self.active = True
        
        # Tamaño según el tipo
        if owner == "player":
            self.size = (8, 16)
            self.sprite = self.sprite_manager.get_sprite("bullet_player", self.size)
        else:
            self.size = (8, 12)
            self.sprite = self.sprite_manager.get_sprite("bullet_alien", self.size)
            
        # Rect para colisiones
        self.rect = pygame.Rect(x - self.size[0]//2, y - self.size[1]//2, self.size[0], self.size[1])
        
        # Efectos visuales
        self.trail_positions = []
        self.trail_max_length = 8
    
    def update(self, dt):
        """Actualizar bala"""
        if not self.active:
            return
            
        # Actualizar posición
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Actualizar rect
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Actualizar rastro
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > self.trail_max_length:
            self.trail_positions.pop(0)
            
        # Actualizar edad
        self.age += dt
        
        # Verificar si debe ser removida
        if self.age >= self.lifetime:
            self.active = False
            
        # Verificar si está fuera de los límites
        if (self.x < -50 or self.x > SCREEN_WIDTH + 50 or
            self.y < -50 or self.y > SCREEN_HEIGHT + 50):
            self.active = False
    
    def draw(self, screen, camera_x, camera_y):
        """Dibujar bala"""
        if not self.active:
            return
            
        # Calcular posición en pantalla
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Dibujar rastro
        if len(self.trail_positions) > 1:
            trail_points = []
            for i, (trail_x, trail_y) in enumerate(self.trail_positions):
                trail_screen_x = trail_x - camera_x
                trail_screen_y = trail_y - camera_y
                
                # Calcular alpha basado en la posición en el rastro
                alpha = int(255 * (i / len(self.trail_positions)) * 0.5)
                
                if alpha > 0:
                    trail_points.append((trail_screen_x, trail_screen_y, alpha))
            
            # Dibujar líneas del rastro
            if len(trail_points) > 1:
                for i in range(len(trail_points) - 1):
                    x1, y1, alpha1 = trail_points[i]
                    x2, y2, alpha2 = trail_points[i + 1]
                    
                    # Color del rastro según el tipo
                    if self.owner == "player":
                        color = (0, 255, 255)  # Cyan
                    else:
                        color = (255, 255, 0)  # Amarillo
                    
                    # Crear surface temporal para el alpha
                    if alpha1 > 0 and alpha2 > 0:
                        avg_alpha = (alpha1 + alpha2) // 2
                        temp_surface = pygame.Surface((abs(x2-x1)+2, abs(y2-y1)+2), pygame.SRCALPHA)
                        temp_surface.set_alpha(avg_alpha)
                        pygame.draw.line(temp_surface, color, (1, 1), (abs(x2-x1)+1, abs(y2-y1)+1), 2)
                        screen.blit(temp_surface, (min(x1, x2), min(y1, y2)))
        
        # Rotar sprite
        rotated_sprite = self.sprite_manager.rotate_sprite(self.sprite, -self.angle)
        
        # Efecto de brillantez
        if self.owner == "player":
            # Efecto de parpadeo para balas del jugador
            brightness = 1.0 + 0.3 * math.sin(self.age * 0.01)
            if brightness > 1.0:
                temp_surface = rotated_sprite.copy()
                temp_surface.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
                alpha = int(255 * (brightness - 1.0))
                temp_surface.set_alpha(alpha)
                rotated_sprite = temp_surface
        
        # Centrar sprite
        sprite_rect = rotated_sprite.get_rect()
        sprite_rect.centerx = screen_x
        sprite_rect.centery = screen_y
        
        screen.blit(rotated_sprite, sprite_rect)
        
        # Dibujar núcleo brillante
        if self.owner == "player":
            pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), 2)
        else:
            pygame.draw.circle(screen, (255, 255, 0), (int(screen_x), int(screen_y)), 1)
            
    def get_rect(self):
        """Obtener rectángulo de colisión"""
        return self.rect
        
    def is_active(self):
        """Verificar si la bala está activa"""
        return self.active
        
    def deactivate(self):
        """Desactivar bala"""
        self.active = False
        
    def get_damage(self):
        """Obtener daño de la bala"""
        return self.damage
        
    def get_owner(self):
        """Obtener propietario de la bala"""
        return self.owner 
"""
Clase de los enemigos alienígenas para Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import math
import random
from .settings import *
from .behavior_tree import AlienBehaviorTree
from .bullet import Bullet

class Alien:
    """Clase que representa a un alienígena enemigo"""
    
    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.sprite_manager = sprite_manager
        self.start_x = x
        self.start_y = y
        
        # Estadísticas
        self.health = ALIEN_HEALTH
        self.max_health = ALIEN_HEALTH
        self.speed = ALIEN_SPEED
        self.size = 32
        
        # Obtener sprite del alien
        self.sprite = self.sprite_manager.get_sprite("alien", (self.size, self.size))
        self.rect = pygame.Rect(x - self.size//2, y - self.size//2, self.size, self.size)
        
        # Movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.target_x = x
        self.target_y = y
        
        # Rotación
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(30, 60)
        
        # IA
        self.behavior_tree = AlienBehaviorTree(self)
        self.detection_range = 150
        self.attack_range = 80
        self.shoot_cooldown = 2000  # 2 segundos
        self.last_shot = 0
        
        # Estados
        self.state = "patrol"
        self.patrol_points = []
        self.current_patrol_index = 0
        self.patrol_wait_time = 0
        
        # Generar puntos de patrulla
        self.generate_patrol_points()
        
        # Pathfinding
        self.path = []
        self.current_path_index = 0
        self.path_update_timer = 0
        
        # Animación
        self.animation_timer = 0
        self.animation_frame = 0
    
    def generate_patrol_points(self):
        """Generar puntos de patrulla alrededor de la posición inicial"""
        num_points = random.randint(3, 5)
        for _ in range(num_points):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, 100)
            px = self.start_x + math.cos(angle) * distance
            py = self.start_y + math.sin(angle) * distance
            
            # Mantener dentro de los límites
            px = max(50, min(SCREEN_WIDTH - 50, px))
            py = max(50, min(SCREEN_HEIGHT - 50, py))
            
            self.patrol_points.append((px, py))
    
    def update(self, dt, player, level_map, bullets, audio_manager):
        """Actualizar alien"""
        # Actualizar comportamiento
        self.behavior_tree.update(dt, player, level_map, bullets, audio_manager)
        
        # Actualizar posición
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Actualizar rect
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Actualizar rotación
        self.angle += self.rotation_speed * dt
        self.angle = self.angle % 360
        
        # Actualizar animación
        self.animation_timer += dt
        if self.animation_timer >= 500:  # Cambiar frame cada 0.5 segundos
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
            
        # Aplicar fricción
        self.vel_x *= 0.9
        self.vel_y *= 0.9
        
        # Actualizar timers
        self.patrol_wait_time = max(0, self.patrol_wait_time - dt)
        self.path_update_timer = max(0, self.path_update_timer - dt)
    
    def move_towards(self, target_x, target_y, speed_multiplier=1.0):
        """Mover hacia un objetivo"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:
            # Normalizar dirección
            dx /= distance
            dy /= distance
            
            # Aplicar velocidad
            move_speed = self.speed * speed_multiplier
            self.vel_x += dx * move_speed * 0.1
            self.vel_y += dy * move_speed * 0.1
            
            # Limitar velocidad
            max_vel = move_speed * 0.8
            vel_length = math.sqrt(self.vel_x*self.vel_x + self.vel_y*self.vel_y)
            if vel_length > max_vel:
                self.vel_x = (self.vel_x / vel_length) * max_vel
                self.vel_y = (self.vel_y / vel_length) * max_vel
                
            return False  # No ha llegado
        return True  # Ha llegado
    
    def get_distance_to_player(self, player):
        """Calcular distancia al jugador"""
        dx = player.x - self.x
        dy = player.y - self.y
        return math.sqrt(dx*dx + dy*dy)
    
    def can_see_player(self, player, level_map):
        """Verificar si puede ver al jugador"""
        distance = self.get_distance_to_player(player)
        if distance > self.detection_range:
            return False
            
        # Verificar línea de visión (simplificado)
        return True
    
    def shoot_at_player(self, player, bullets, audio_manager):
        """Disparar al jugador"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot < self.shoot_cooldown:
            return False
            
        # Calcular dirección hacia el jugador
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > self.attack_range:
            return False
            
        # Crear bala
        angle = math.degrees(math.atan2(dy, dx))
        bullet_x = self.x + (dx/distance) * (self.size//2 + 5)
        bullet_y = self.y + (dy/distance) * (self.size//2 + 5)
        
        bullet = Bullet(bullet_x, bullet_y, angle, "alien", self.sprite_manager)
        bullets.append(bullet)
        
        self.last_shot = current_time
        audio_manager.play_sound("alien_shoot")
        
        return True
    
    def patrol(self, dt):
        """Lógica de patrulla"""
        if not self.patrol_points:
            return
            
        # Obtener punto de patrulla actual
        if self.current_patrol_index >= len(self.patrol_points):
            self.current_patrol_index = 0
            
        target_x, target_y = self.patrol_points[self.current_patrol_index]
        
        # Mover hacia el punto
        if self.move_towards(target_x, target_y, 0.5):
            # Ha llegado al punto
            self.patrol_wait_time = 1000  # Esperar 1 segundo
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
            
    def flee_from_player(self, player):
        """Huir del jugador"""
        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Huir en dirección opuesta
            dx /= distance
            dy /= distance
            
            flee_x = self.x + dx * 100
            flee_y = self.y + dy * 100
            
            # Mantener dentro de los límites
            flee_x = max(50, min(SCREEN_WIDTH - 50, flee_x))
            flee_y = max(50, min(SCREEN_HEIGHT - 50, flee_y))
            
            self.move_towards(flee_x, flee_y, 1.5)
            
    def take_damage(self, damage, audio_manager):
        """Recibir daño"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            audio_manager.play_sound("alien_death")
            return True  # Alien murió
        else:
            audio_manager.play_sound("alien_hit")
            return False
            
    def is_dead(self):
        """Verificar si está muerto"""
        return self.health <= 0
    
    def draw(self, screen, camera_x, camera_y):
        """Dibujar alien"""
        # Calcular posición en pantalla
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Rotar sprite
        rotated_sprite = self.sprite_manager.rotate_sprite(self.sprite, self.angle)
        
        # Efecto de animación (escala pulsante)
        scale_factor = 1.0 + 0.1 * math.sin(self.animation_timer * 0.01)
        if scale_factor != 1.0:
            rotated_sprite = self.sprite_manager.scale_sprite(rotated_sprite, scale_factor)
        
        # Centrar sprite
        sprite_rect = rotated_sprite.get_rect()
        sprite_rect.centerx = screen_x
        sprite_rect.centery = screen_y
        
        screen.blit(rotated_sprite, sprite_rect)
        
        # Dibujar barra de salud si está dañado
        if self.health < self.max_health:
            health_bar_width = 30
            health_bar_height = 4
            health_x = screen_x - health_bar_width // 2
            health_y = screen_y - self.size // 2 - 8
            
            # Fondo de la barra
            pygame.draw.rect(screen, (255, 0, 0), 
                           (health_x, health_y, health_bar_width, health_bar_height))
            
            # Barra de salud
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (255, 255, 0), 
                           (health_x, health_y, health_bar_width * health_ratio, health_bar_height))
                           
        # Dibujar indicador de estado (debug)
        if DEBUG:
            font = pygame.font.Font(None, 16)
            state_text = font.render(self.state, True, (255, 255, 255))
            screen.blit(state_text, (screen_x - 20, screen_y + self.size//2 + 5))
    
    def get_rect(self):
        """Obtener rectángulo de colisión"""
        return self.rect 
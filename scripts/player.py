"""
Clase del jugador para Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import math
from .settings import *
from .bullet import Bullet

class Player:
    """Clase que representa al jugador"""
    
    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.sprite_manager = sprite_manager
        self.angle = 0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.ammo = PLAYER_AMMO
        self.max_ammo = PLAYER_AMMO
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.last_shot = 0
        self.shot_cooldown = 250  # milisegundos
        self.size = 32
        
        # Obtener sprite del jugador
        self.sprite = self.sprite_manager.get_sprite("player", (self.size, self.size))
        self.rect = pygame.Rect(x - self.size//2, y - self.size//2, self.size, self.size)
        
        # Velocidad actual
        self.vel_x = 0
        self.vel_y = 0
        
        # Rotación suave
        self.target_angle = 0
        self.rotation_speed = 8  # Aumentado para respuesta más rápida
        
        # Sistema de apuntado
        self.aiming_mode = "movement"  # "movement", "mouse", "gamepad"
        self.last_movement_angle = 0
        self.mouse_aim_enabled = False
        
        # Sistema anti-atascamiento
        self.last_movement_time = 0
        self.no_movement_counter = 0
        self.stuck_threshold = 3000  # 3 segundos sin movimiento
        self.last_position = (x, y)
        
    def update(self, dt, camera_x=0, camera_y=0):
        """Actualizar jugador"""
        # Actualizar posición
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Mantener dentro de los límites del mapa con mejor lógica
        world_width = MAP_WIDTH * TILE_SIZE
        world_height = MAP_HEIGHT * TILE_SIZE
        margin = self.size // 2
        
        # Límites con detección de velocidad para evitar trabarse
        if self.x < margin:
            self.x = margin
            self.vel_x = max(0, self.vel_x)  # Solo permitir velocidad positiva
        elif self.x > world_width - margin:
            self.x = world_width - margin
            self.vel_x = min(0, self.vel_x)  # Solo permitir velocidad negativa
            
        if self.y < margin:
            self.y = margin
            self.vel_y = max(0, self.vel_y)  # Solo permitir velocidad positiva
        elif self.y > world_height - margin:
            self.y = world_height - margin
            self.vel_y = min(0, self.vel_y)  # Solo permitir velocidad negativa
        
        # Actualizar rect
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # Actualizar rotación con mouse
        self.update_mouse_aim(camera_x, camera_y)
        
        # Rotación suave hacia el objetivo
        angle_diff = self.target_angle - self.angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
            
        self.angle += angle_diff * self.rotation_speed * dt
        self.angle = self.angle % 360
        
        # Actualizar invulnerabilidad
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                
        # Aplicar fricción (reducida para mejor control)
        friction = 0.9  # Aumentado para reducir la fricción
        self.vel_x *= friction
        self.vel_y *= friction
        
        # Detener movimiento muy lento para evitar vibración - SOLO si no hay entrada activa
        # Esto previene que el jugador se quede atascado
        min_velocity_threshold = 0.5  # Reducido para permitir movimientos más lentos
        if abs(self.vel_x) < min_velocity_threshold:
            self.vel_x = 0
        if abs(self.vel_y) < min_velocity_threshold:
            self.vel_y = 0
            
        # Sistema anti-atascamiento
        current_time = pygame.time.get_ticks()
        position_changed = abs(self.x - self.last_position[0]) > 2 or abs(self.y - self.last_position[1]) > 2
        
        if position_changed:
            self.last_movement_time = current_time
            self.no_movement_counter = 0
            self.last_position = (self.x, self.y)
        elif current_time - self.last_movement_time > self.stuck_threshold:
            # El jugador está atascado, aplicar pequeño empuje aleatorio
            if self.no_movement_counter < 3:  # Máximo 3 intentos
                if DEBUG:
                    print("DEBUG: Jugador detectado como atascado, aplicando desbloqueo automático")
                import random
                push_x = random.uniform(-20, 20)
                push_y = random.uniform(-20, 20)
                self.vel_x = push_x
                self.vel_y = push_y
                self.no_movement_counter += 1
                self.last_movement_time = current_time
        
    def update_mouse_aim(self, camera_x, camera_y):
        """Actualizar apuntado con mouse"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Convertir posición del mouse a coordenadas del mundo
        world_mouse_x = mouse_x + camera_x
        world_mouse_y = mouse_y + camera_y
        
        # Calcular ángulo desde el jugador al mouse
        dx = world_mouse_x - self.x
        dy = world_mouse_y - self.y
        
        # Si el mouse está muy cerca, usar la última dirección de movimiento
        mouse_distance = math.sqrt(dx*dx + dy*dy)
        if mouse_distance > 20:  # Zona muerta para evitar jitter
            mouse_angle = math.degrees(math.atan2(dy, dx)) - 90
            self.target_angle = mouse_angle
            self.aiming_mode = "mouse"
            self.mouse_aim_enabled = True
        elif not self.mouse_aim_enabled:
            # Si el mouse no está activo, usar dirección de movimiento
            self.target_angle = self.last_movement_angle
            self.aiming_mode = "movement"
    
    def update_gamepad_aim(self, gamepad):
        """Actualizar apuntado con stick derecho del gamepad"""
        if not gamepad:
            return
            
        try:
            # Stick derecho (ejes 2 y 3 normalmente)
            if gamepad.get_numaxes() >= 4:
                aim_x = gamepad.get_axis(2)  # Stick derecho X
                aim_y = gamepad.get_axis(3)  # Stick derecho Y
                
                # Zona muerta para el stick derecho
                deadzone = 0.3
                if abs(aim_x) > deadzone or abs(aim_y) > deadzone:
                    gamepad_angle = math.degrees(math.atan2(aim_y, aim_x)) - 90
                    self.target_angle = gamepad_angle
                    self.aiming_mode = "gamepad"
                    self.mouse_aim_enabled = False
                    
        except Exception as e:
            print(f"Error leyendo stick derecho: {e}")
        
    def move(self, dx, dy):
        """Mover jugador"""
        if dx != 0 or dy != 0:
            # Normalizar movimiento diagonal
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                dx /= length
                dy /= length
                
            # Aplicar velocidad con mayor responsividad
            acceleration = self.speed * 0.15  # Aumentado para mejor respuesta
            self.vel_x += dx * acceleration
            self.vel_y += dy * acceleration
            
            # Limitar velocidad máxima
            max_vel = self.speed * 0.9  # Aumentado ligeramente
            vel_length = math.sqrt(self.vel_x*self.vel_x + self.vel_y*self.vel_y)
            if vel_length > max_vel:
                self.vel_x = (self.vel_x / vel_length) * max_vel
                self.vel_y = (self.vel_y / vel_length) * max_vel
                
            # Actualizar ángulo de movimiento
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                movement_angle = math.degrees(math.atan2(dy, dx)) - 90
                self.last_movement_angle = movement_angle
                
                # Solo actualizar target_angle si no estamos usando mouse/gamepad
                if self.aiming_mode == "movement":
                    self.target_angle = movement_angle
                    
    def shoot(self, bullets, audio_manager):
        """Disparar bala"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_cooldown and self.ammo > 0:
            # Calcular posición de disparo
            angle_rad = math.radians(self.angle + 90)
            bullet_x = self.x + math.cos(angle_rad) * (self.size//2 + 5)
            bullet_y = self.y + math.sin(angle_rad) * (self.size//2 + 5)
            
            # Crear bala
            bullet = Bullet(bullet_x, bullet_y, self.angle, "player", self.sprite_manager)
            bullets.append(bullet)
            
            self.ammo -= 1
            self.last_shot = current_time
            
            # Reproducir sonido
            audio_manager.play_sound("shoot")
            
            # Retroceso
            recoil_force = 50
            recoil_x = -math.cos(angle_rad) * recoil_force * 0.01
            recoil_y = -math.sin(angle_rad) * recoil_force * 0.01
            self.vel_x += recoil_x
            self.vel_y += recoil_y
            
    def take_damage(self, damage, audio_manager):
        """Recibir daño"""
        if not self.invulnerable:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                audio_manager.play_sound("player_death")
                return True  # Jugador murió
            else:
                # Activar invulnerabilidad temporal
                self.invulnerable = True
                self.invulnerable_timer = 1000  # 1 segundo
                audio_manager.play_sound("player_hit")
                return False
                
    def heal(self, amount):
        """Curar jugador"""
        self.health = min(self.max_health, self.health + amount)
        
    def add_ammo(self, amount):
        """Agregar munición"""
        self.ammo = min(self.max_ammo, self.ammo + amount)
        
    def draw(self, screen, camera_x, camera_y):
        """Dibujar jugador"""
        # Calcular posición en pantalla
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Rotar sprite
        rotated_sprite = self.sprite_manager.rotate_sprite(self.sprite, -self.angle)
        
        # Efecto de parpadeo si es invulnerable
        if self.invulnerable:
            alpha = 128 if (pygame.time.get_ticks() // 100) % 2 else 255
            temp_surface = rotated_sprite.copy()
            temp_surface.set_alpha(alpha)
            rotated_sprite = temp_surface
            
        # Centrar sprite
        sprite_rect = rotated_sprite.get_rect()
        sprite_rect.centerx = screen_x
        sprite_rect.centery = screen_y
        
        screen.blit(rotated_sprite, sprite_rect)
        
        # Dibujar indicador de dirección de apuntado
        if self.aiming_mode == "mouse":
            # Dibujar pequeño indicador verde para mostrar que está apuntando con mouse
            aim_x = screen_x + math.cos(math.radians(self.angle + 90)) * (self.size//2 + 10)
            aim_y = screen_y + math.sin(math.radians(self.angle + 90)) * (self.size//2 + 10)
            pygame.draw.circle(screen, (0, 255, 0), (int(aim_x), int(aim_y)), 3)
        elif self.aiming_mode == "gamepad":
            # Dibujar pequeño indicador azul para gamepad
            aim_x = screen_x + math.cos(math.radians(self.angle + 90)) * (self.size//2 + 10)
            aim_y = screen_y + math.sin(math.radians(self.angle + 90)) * (self.size//2 + 10)
            pygame.draw.circle(screen, (0, 0, 255), (int(aim_x), int(aim_y)), 3)
        
        # Dibujar indicador de salud si está dañado
        if self.health < self.max_health:
            health_bar_width = 40
            health_bar_height = 6
            health_x = screen_x - health_bar_width // 2
            health_y = screen_y - self.size // 2 - 10
            
            # Fondo de la barra
            pygame.draw.rect(screen, (255, 0, 0), 
                           (health_x, health_y, health_bar_width, health_bar_height))
            
            # Barra de salud
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (0, 255, 0), 
                           (health_x, health_y, health_bar_width * health_ratio, health_bar_height))
            
    def get_rect(self):
        """Obtener rectángulo de colisión"""
        return self.rect
        
    def is_dead(self):
        """Verificar si el jugador está muerto"""
        return self.health <= 0 
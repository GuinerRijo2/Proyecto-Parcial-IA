"""
Clase del nivel de juego para Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import random
import math
from .settings import *
from .player import Player
from .alien import Alien
from .a_star import AStar
from .sprite_manager import SpriteManager

class Level:
    """Clase que maneja el nivel actual del juego"""
    
    def __init__(self, game):
        self.game = game
        self.game_over = False
        self.victory = False
        
        # Sistemas
        self.sprite_manager = SpriteManager()
        
        # Mapa
        self.map_data = self.generate_map()
        self.pathfinder = AStar(self.map_data)
        
        # Cámara
        self.camera_x = 0
        self.camera_y = 0
        
        # Jugador
        start_x, start_y = self.find_spawn_position()
        self.player = Player(start_x, start_y, self.sprite_manager)
        
        # Enemigos
        self.aliens = []
        self.spawn_aliens()
        
        # Balas
        self.bullets = []
        
        # Objetivos del nivel
        self.aliens_killed = 0
        self.aliens_to_kill = len(self.aliens)
        
        # Tiempo
        self.level_time = 0
        
        print(f"Nivel cargado: {len(self.aliens)} aliens generados")
    
    def generate_map(self):
        """Generar un mapa básico"""
        # Crear mapa lleno de suelo
        map_data = [[FLOOR_TILE for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # Agregar paredes en los bordes
        for x in range(MAP_WIDTH):
            map_data[0][x] = WALL_TILE  # Arriba
            map_data[MAP_HEIGHT - 1][x] = WALL_TILE  # Abajo
        
        for y in range(MAP_HEIGHT):
            map_data[y][0] = WALL_TILE  # Izquierda
            map_data[y][MAP_WIDTH - 1] = WALL_TILE  # Derecha
        
        # Agregar algunas paredes internas para crear un laberinto simple
        for _ in range(30):  # 30 paredes aleatorias
            x = random.randint(2, MAP_WIDTH - 3)
            y = random.randint(2, MAP_HEIGHT - 3)
            
            # Crear pequeños bloques de paredes
            for dx in range(random.randint(1, 3)):
                for dy in range(random.randint(1, 3)):
                    if (x + dx < MAP_WIDTH - 1 and y + dy < MAP_HEIGHT - 1):
                        map_data[y + dy][x + dx] = WALL_TILE
        
        # Asegurar que el área de spawn del jugador esté libre
        spawn_area_x = MAP_WIDTH // 4
        spawn_area_y = MAP_HEIGHT // 4
        for x in range(spawn_area_x - 2, spawn_area_x + 3):
            for y in range(spawn_area_y - 2, spawn_area_y + 3):
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    map_data[y][x] = FLOOR_TILE
        
        return map_data
    
    def find_spawn_position(self):
        """Encontrar una posición de spawn válida"""
        # Buscar posición libre en el área de spawn
        for attempt in range(100):
            x = random.randint(2, MAP_WIDTH // 2)
            y = random.randint(2, MAP_HEIGHT // 2)
            
            if self.map_data[y][x] == FLOOR_TILE:
                world_x = x * TILE_SIZE + TILE_SIZE // 2
                world_y = y * TILE_SIZE + TILE_SIZE // 2
                return world_x, world_y
        
        # Fallback: centro del mapa
        return MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2
    
    def spawn_aliens(self):
        """Generar aliens en el mapa"""
        alien_count = random.randint(8, 15)
        
        for _ in range(alien_count):
            # Encontrar posición válida lejos del jugador
            for attempt in range(100):
                x = random.randint(1, MAP_WIDTH - 2)
                y = random.randint(1, MAP_HEIGHT - 2)
                
                if self.map_data[y][x] == FLOOR_TILE:
                    world_x = x * TILE_SIZE + TILE_SIZE // 2
                    world_y = y * TILE_SIZE + TILE_SIZE // 2
                    
                    # Verificar distancia al jugador
                    dx = world_x - self.player.x
                    dy = world_y - self.player.y
                    distance = math.sqrt(dx * dx + dy * dy)
                    
                    if distance > 150:  # Suficientemente lejos del jugador
                        alien = Alien(world_x, world_y, self.sprite_manager)
                        self.aliens.append(alien)
                        break
    
    def handle_event(self, event):
        """Manejar eventos del nivel"""
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_PAUSE:
                self.game.state = GAME_STATE_PAUSED
    
    def update(self, dt):
        """Actualizar lógica del nivel"""
        if self.game_over:
            return
        
        current_time = pygame.time.get_ticks() / 1000.0
        self.level_time += dt
        
        # Actualizar cámara primero
        self.update_camera()
        
        # Actualizar jugador con información de cámara
        self.player.update(dt, self.camera_x, self.camera_y)
        
        # Actualizar apuntado con gamepad si está disponible
        if self.game.input_handler.gamepad:
            self.player.update_gamepad_aim(self.game.input_handler.gamepad)
        
        # Verificar si el jugador murió
        if self.player.is_dead():
            self.game_over = True
            return
        
        # Actualizar aliens
        for alien in self.aliens[:]:
            alien.update(dt, self.player, self.map_data, self.bullets, self.game.audio_manager)
            
            # Remover aliens muertos
            if alien.is_dead():
                self.aliens.remove(alien)
                self.aliens_killed += 1
        
        # Actualizar balas
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if not bullet.is_active():
                self.bullets.remove(bullet)
        
        # Manejar entrada del jugador
        self.handle_input()
        
        # Verificar condición de victoria
        if len(self.aliens) == 0:
            self.victory = True
            self.game_over = True
        
        # Verificar colisiones
        self.check_collisions(dt)
    
    def handle_input(self):
        """Manejar entrada del jugador"""
        input_handler = self.game.input_handler
        
        # Movimiento
        move_x, move_y = input_handler.get_movement_vector()
        self.player.move(move_x, move_y)
        
        # Disparo
        if input_handler.is_shooting():
            self.player.shoot(self.bullets, self.game.audio_manager)
            
        # Debug: Imprimir información si no hay movimiento pero debería haberlo
        if DEBUG and (abs(move_x) > 0.1 or abs(move_y) > 0.1):
            if abs(self.player.vel_x) < 0.1 and abs(self.player.vel_y) < 0.1:
                print(f"DEBUG: Entrada detectada ({move_x:.2f}, {move_y:.2f}) pero jugador sin velocidad")
                print(f"DEBUG: Velocidad del jugador: ({self.player.vel_x:.2f}, {self.player.vel_y:.2f})")
                print(f"DEBUG: Posición del jugador: ({self.player.x:.1f}, {self.player.y:.1f})")
                input_info = input_handler.get_input_info()
                print(f"DEBUG: Entrada completa: {input_info}")
                print("---")
    
    def update_camera(self):
        """Actualizar posición de la cámara"""
        # Seguir al jugador
        target_x = self.player.x - SCREEN_WIDTH // 2
        target_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Suavizar movimiento de cámara
        lerp_factor = 0.1
        self.camera_x += (target_x - self.camera_x) * lerp_factor
        self.camera_y += (target_y - self.camera_y) * lerp_factor
        
        # Limitar cámara a los bordes del mapa
        max_camera_x = MAP_WIDTH * TILE_SIZE - SCREEN_WIDTH
        max_camera_y = MAP_HEIGHT * TILE_SIZE - SCREEN_HEIGHT
        
        self.camera_x = max(0, min(max_camera_x, self.camera_x))
        self.camera_y = max(0, min(max_camera_y, self.camera_y))
    
    def check_collisions(self, dt):
        """Verificar todas las colisiones"""
        # Colisiones jugador-alien
        player_rect = self.player.get_rect()
        
        for alien in self.aliens:
            if not alien.is_dead():
                alien_rect = alien.get_rect()
                if player_rect.colliderect(alien_rect):
                    # Daño por contacto
                    if self.player.take_damage(5, self.game.audio_manager):
                        self.game_over = True
                        return
        
        # Colisiones balas
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            
            if bullet.get_owner() == "player":
                # Balas del jugador vs aliens
                for alien in self.aliens:
                    if not alien.is_dead():
                        alien_rect = alien.get_rect()
                        if bullet_rect.colliderect(alien_rect):
                            alien.take_damage(bullet.get_damage(), self.game.audio_manager)
                            bullet.deactivate()
                            break
            else:
                # Balas de aliens vs jugador
                if bullet_rect.colliderect(player_rect):
                    if self.player.take_damage(bullet.get_damage(), self.game.audio_manager):
                        self.game_over = True
                        return
                    bullet.deactivate()
            
            # Balas vs paredes
            if self.check_wall_collision(bullet.x, bullet.y):
                bullet.deactivate()
        
        # Colisiones con paredes para entidades
        self.check_entity_wall_collisions(dt)
    
    def check_wall_collision(self, x, y):
        """Verificar colisión con paredes en una posición"""
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        
        if (grid_x < 0 or grid_x >= MAP_WIDTH or 
            grid_y < 0 or grid_y >= MAP_HEIGHT):
            return True
        
        return self.map_data[grid_y][grid_x] == WALL_TILE
    
    def check_entity_wall_collisions(self, dt):
        """Verificar colisiones de entidades con paredes"""
        # Jugador vs paredes - mejorado para evitar trabarse
        self.resolve_player_wall_collision(dt)
        
        # Aliens vs paredes
        for alien in self.aliens:
            self.resolve_alien_wall_collision(alien, dt)
    
    def resolve_player_wall_collision(self, dt):
        """Resolver colisiones del jugador con paredes de manera más suave"""
        player = self.player
        
        # Guardar posición y velocidad actuales
        old_x = player.x
        old_y = player.y
        old_vel_x = player.vel_x
        old_vel_y = player.vel_y
        
        # Actualizar rect del jugador
        player.rect.centerx = player.x
        player.rect.centery = player.y
        
        # Verificar colisión
        if self.is_rect_in_wall(player.rect):
            if DEBUG:
                print(f"DEBUG: Colisión detectada en ({player.x:.1f}, {player.y:.1f})")
                print(f"DEBUG: Velocidad antes: ({old_vel_x:.2f}, {old_vel_y:.2f})")
            
            # Sistema de deslizamiento a lo largo de paredes
            collision_resolved = False
            
            # Intentar movimiento solo en X (mantener Y anterior)
            player.y = old_y
            player.rect.centery = player.y
            
            if not self.is_rect_in_wall(player.rect):
                # Puede moverse en X, bloquear solo Y
                player.vel_y = 0
                collision_resolved = True
                if DEBUG:
                    print("DEBUG: Permitiendo movimiento en X, bloqueando Y")
            else:
                # Restaurar Y y intentar movimiento solo en Y
                player.y = old_y + old_vel_y * dt
                player.x = old_x
                player.rect.centerx = player.x
                player.rect.centery = player.y
                
                if not self.is_rect_in_wall(player.rect):
                    # Puede moverse en Y, bloquear solo X
                    player.vel_x = 0
                    collision_resolved = True
                    if DEBUG:
                        print("DEBUG: Permitiendo movimiento en Y, bloqueando X")
                else:
                    # No puede moverse en ninguna dirección, revertir posición
                    player.x = old_x
                    player.y = old_y
                    
                    # Aplicar fricción a las velocidades en lugar de resetear a 0
                    player.vel_x *= 0.5
                    player.vel_y *= 0.5
                    
                    if DEBUG:
                        print(f"DEBUG: Bloqueando ambas direcciones, aplicando fricción")
                        print(f"DEBUG: Nueva velocidad: ({player.vel_x:.2f}, {player.vel_y:.2f})")
                    
                    # Si las velocidades son muy pequeñas, permitir un pequeño empuje
                    if abs(player.vel_x) < 5 and abs(player.vel_y) < 5:
                        # Empujar ligeramente hacia el centro del tile más cercano
                        tile_x = int(old_x // TILE_SIZE)
                        tile_y = int(old_y // TILE_SIZE)
                        tile_center_x = tile_x * TILE_SIZE + TILE_SIZE // 2
                        tile_center_y = tile_y * TILE_SIZE + TILE_SIZE // 2
                        
                        push_x = (tile_center_x - old_x) * 0.1
                        push_y = (tile_center_y - old_y) * 0.1
                        
                        # Verificar que el empuje sea seguro
                        test_x = old_x + push_x
                        test_y = old_y + push_y
                        player.x = test_x
                        player.y = test_y
                        player.rect.centerx = player.x
                        player.rect.centery = player.y
                        
                        if self.is_rect_in_wall(player.rect):
                            # El empuje no es seguro, mantener posición original
                            player.x = old_x
                            player.y = old_y
                            if DEBUG:
                                print("DEBUG: Empuje no seguro, manteniendo posición")
                        else:
                            # El empuje es seguro, aplicar pequeña velocidad
                            player.vel_x = push_x * 2
                            player.vel_y = push_y * 2
                            if DEBUG:
                                print(f"DEBUG: Empuje aplicado: ({push_x*2:.2f}, {push_y*2:.2f})")
        
        # Actualizar rect final
        player.rect.centerx = player.x
        player.rect.centery = player.y
    
    def resolve_alien_wall_collision(self, alien, dt):
        """Resolver colisiones de aliens con paredes"""
        alien_rect = alien.get_rect()
        if self.is_rect_in_wall(alien_rect):
            # Revertir movimiento del alien
            alien.x -= alien.vel_x * dt
            alien.y -= alien.vel_y * dt
            
            # Resetear velocidad para evitar quedarse atascado
            alien.vel_x = 0
            alien.vel_y = 0
            
            # Actualizar rect
            alien.rect.centerx = alien.x
            alien.rect.centery = alien.y
    
    def is_rect_in_wall(self, rect):
        """Verificar si un rectángulo está en una pared"""
        # Usar un enfoque más flexible - verificar el centro y algunos puntos clave
        # En lugar de las 4 esquinas exactas que pueden ser demasiado restrictivas
        
        # Reducir ligeramente el área de colisión para mejor jugabilidad
        margin = 2
        test_rect = pygame.Rect(rect.left + margin, rect.top + margin, 
                               rect.width - 2*margin, rect.height - 2*margin)
        
        # Verificar puntos clave del rectángulo ajustado
        test_points = [
            (test_rect.left, test_rect.top),           # Esquina superior izquierda
            (test_rect.right - 1, test_rect.top),      # Esquina superior derecha
            (test_rect.left, test_rect.bottom - 1),    # Esquina inferior izquierda
            (test_rect.right - 1, test_rect.bottom - 1), # Esquina inferior derecha
            (test_rect.centerx, test_rect.centery),    # Centro
        ]
        
        # Solo consideramos colisión si al menos 2 puntos están en pared
        # Esto permite mejor movimiento cerca de esquinas
        wall_hits = 0
        for x, y in test_points:
            if self.check_wall_collision(x, y):
                wall_hits += 1
                
        # Requiere al menos 2 puntos en pared para considerar colisión
        return wall_hits >= 2
    
    def draw(self, screen):
        """Dibujar el nivel"""
        # Dibujar mapa
        self.draw_map(screen)
        
        # Dibujar aliens
        for alien in self.aliens:
            alien.draw(screen, self.camera_x, self.camera_y)
        
        # Dibujar balas
        for bullet in self.bullets:
            bullet.draw(screen, self.camera_x, self.camera_y)
        
        # Dibujar jugador
        self.player.draw(screen, self.camera_x, self.camera_y)
        
        # Dibujar HUD
        self.draw_hud(screen)
    
    def draw_map(self, screen):
        """Dibujar el mapa de tiles"""
        # Calcular tiles visibles
        start_x = max(0, int(self.camera_x // TILE_SIZE))
        end_x = min(MAP_WIDTH, int((self.camera_x + SCREEN_WIDTH) // TILE_SIZE) + 1)
        start_y = max(0, int(self.camera_y // TILE_SIZE))
        end_y = min(MAP_HEIGHT, int((self.camera_y + SCREEN_HEIGHT) // TILE_SIZE) + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_type = self.map_data[y][x]
                
                # Calcular posición en pantalla
                screen_x = x * TILE_SIZE - self.camera_x
                screen_y = y * TILE_SIZE - self.camera_y
                
                # Obtener sprite apropiado
                if tile_type == WALL_TILE:
                    sprite = self.sprite_manager.get_sprite("wall", (TILE_SIZE, TILE_SIZE))
                else:  # FLOOR_TILE
                    sprite = self.sprite_manager.get_sprite("floor", (TILE_SIZE, TILE_SIZE))
                
                screen.blit(sprite, (screen_x, screen_y))
    
    def draw_hud(self, screen):
        """Dibujar HUD del nivel"""
        # HUD del jugador
        font = pygame.font.Font(None, 36)
        
        # Salud del jugador
        health_icon = self.sprite_manager.get_sprite("health_icon", (24, 24))
        screen.blit(health_icon, (20, 20))
        health_text = font.render(f"{self.player.health}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (55, 25))
        
        # Munición del jugador
        ammo_icon = self.sprite_manager.get_sprite("ammo_icon", (24, 24))
        screen.blit(ammo_icon, (20, 60))
        ammo_text = font.render(f"{self.player.ammo}", True, WHITE)
        screen.blit(ammo_text, (55, 65))
        
        # Información del nivel
        # Contador de aliens
        aliens_text = font.render(f"Aliens: {len(self.aliens)}", True, WHITE)
        screen.blit(aliens_text, (SCREEN_WIDTH - 200, 20))
        
        # Tiempo
        minutes = int(self.level_time // 60)
        seconds = int(self.level_time % 60)
        time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 200, 60))
        
        # Mensaje de victoria/derrota
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 74)
            
            if self.victory:
                text = big_font.render("VICTORY!", True, GREEN)
                subtext = font.render("All aliens eliminated!", True, WHITE)
            else:
                text = big_font.render("GAME OVER", True, RED)
                subtext = font.render("You have been killed!", True, WHITE)
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            subtext_rect = subtext.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            screen.blit(text, text_rect)
            screen.blit(subtext, subtext_rect)
            
            # Instrucciones
            restart_text = font.render("Press ESC to return to menu", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(restart_text, restart_rect) 
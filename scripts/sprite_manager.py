"""
Sistema de manejo de sprites para Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import pygame
import math
import os
from typing import Dict, Optional
from .settings import *

# Deshabilitar cairosvg temporalmente debido a problemas con Cairo en Windows
SVG_SUPPORT = False
# Intentar importar cairosvg
# try:
#     import cairosvg
#     from PIL import Image
#     import io
#     SVG_SUPPORT = True
# except ImportError:
#     SVG_SUPPORT = False

class SpriteManager:
    """Clase para manejar todos los sprites del juego"""
    
    def __init__(self):
        self.sprites: Dict[str, pygame.Surface] = {}
        self.loaded_svgs: Dict[str, pygame.Surface] = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Cargar todos los sprites del juego"""
        # Intentar cargar sprites desde archivos, si no existen crear sprites sintéticos
        self.load_player_sprites()
        self.load_alien_sprites()
        self.load_bullet_sprites()
        self.load_ui_sprites()
    
    def load_player_sprites(self):
        """Cargar sprites del jugador"""
        player_sprite_path = "assets/images/player.png"
        
        if os.path.exists(player_sprite_path):
            try:
                sprite = pygame.image.load(player_sprite_path).convert_alpha()
                self.sprites["player"] = pygame.transform.scale(sprite, (24, 24))
                print("Sprite del jugador cargado desde archivo")
                return
            except Exception as e:
                print(f"Error cargando sprite del jugador: {e}")
        
        # Crear sprite sintético del jugador
        self.sprites["player"] = self.create_player_sprite()
        print("Sprite sintético del jugador creado")
    
    def load_alien_sprites(self):
        """Cargar sprites de los aliens"""
        alien_sprite_path = "assets/images/alien.png"
        
        if os.path.exists(alien_sprite_path):
            try:
                sprite = pygame.image.load(alien_sprite_path).convert_alpha()
                self.sprites["alien"] = pygame.transform.scale(sprite, (24, 24))
                print("Sprite del alien cargado desde archivo")
                return
            except Exception as e:
                print(f"Error cargando sprite del alien: {e}")
        
        # Crear sprite sintético del alien
        self.sprites["alien"] = self.create_alien_sprite()
        print("Sprite sintético del alien creado")
    
    def load_bullet_sprites(self):
        """Cargar sprites de las balas"""
        # Balas del jugador
        player_bullet_path = "assets/images/player_bullet.png"
        if os.path.exists(player_bullet_path):
            try:
                sprite = pygame.image.load(player_bullet_path).convert_alpha()
                self.sprites["player_bullet"] = pygame.transform.scale(sprite, (4, 4))
            except Exception as e:
                print(f"Error cargando sprite de bala del jugador: {e}")
                self.sprites["player_bullet"] = self.create_bullet_sprite(YELLOW)
        else:
            self.sprites["player_bullet"] = self.create_bullet_sprite(YELLOW)
        
        # Balas de los aliens
        alien_bullet_path = "assets/images/alien_bullet.png"
        if os.path.exists(alien_bullet_path):
            try:
                sprite = pygame.image.load(alien_bullet_path).convert_alpha()
                self.sprites["alien_bullet"] = pygame.transform.scale(sprite, (4, 4))
            except Exception as e:
                print(f"Error cargando sprite de bala del alien: {e}")
                self.sprites["alien_bullet"] = self.create_bullet_sprite(RED)
        else:
            self.sprites["alien_bullet"] = self.create_bullet_sprite(RED)
    
    def load_ui_sprites(self):
        """Cargar sprites de la interfaz"""
        # Por ahora no hay sprites de UI específicos
        pass
    
    def create_player_sprite(self):
        """Crear sprite sintético del jugador"""
        sprite = pygame.Surface((24, 24), pygame.SRCALPHA)
        
        # Cuerpo principal (triángulo)
        points = [
            (20, 12),  # Punta (frente)
            (4, 6),    # Esquina superior trasera
            (4, 18)    # Esquina inferior trasera
        ]
        pygame.draw.polygon(sprite, WHITE, points)
        pygame.draw.polygon(sprite, GRAY, points, 2)
        
        # Detalles
        pygame.draw.circle(sprite, BLUE, (8, 12), 3)  # Cabina
        pygame.draw.circle(sprite, WHITE, (8, 12), 3, 1)
        
        return sprite
    
    def create_alien_sprite(self):
        """Crear sprite sintético del alien"""
        sprite = pygame.Surface((24, 24), pygame.SRCALPHA)
        
        # Cuerpo principal (óvalo)
        pygame.draw.ellipse(sprite, RED, (2, 6, 20, 12))
        pygame.draw.ellipse(sprite, DARK_GRAY, (2, 6, 20, 12), 2)
        
        # Cabeza
        pygame.draw.circle(sprite, RED, (12, 8), 4)
        pygame.draw.circle(sprite, DARK_GRAY, (12, 8), 4, 1)
        
        # Ojos
        pygame.draw.circle(sprite, YELLOW, (10, 6), 2)
        pygame.draw.circle(sprite, YELLOW, (14, 6), 2)
        pygame.draw.circle(sprite, BLACK, (10, 6), 1)
        pygame.draw.circle(sprite, BLACK, (14, 6), 1)
        
        # Extremidades
        for i in range(3):
            y_offset = 4 + i * 4
            pygame.draw.line(sprite, RED, (2, y_offset), (0, y_offset - 2), 2)
            pygame.draw.line(sprite, RED, (22, y_offset), (24, y_offset - 2), 2)
        
        return sprite
    
    def create_bullet_sprite(self, color):
        """Crear sprite sintético de bala"""
        sprite = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(sprite, color, (2, 2), 2)
        pygame.draw.circle(sprite, WHITE, (2, 2), 2, 1)
        return sprite
    
    def create_explosion_sprite(self, size, color):
        """Crear sprite de explosión"""
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        # Círculos concéntricos para efecto de explosión
        for i in range(3):
            radius = center - i * 3
            alpha = 255 - i * 80
            color_with_alpha = (*color, alpha)
            pygame.draw.circle(sprite, color_with_alpha, (center, center), radius)
        
        return sprite
    
    def get_player_sprite(self):
        """Obtener sprite del jugador"""
        return self.sprites.get("player")
    
    def get_alien_sprite(self):
        """Obtener sprite del alien"""
        return self.sprites.get("alien")
    
    def get_bullet_sprite(self, owner):
        """Obtener sprite de bala según el propietario"""
        if owner == "player":
            return self.sprites.get("player_bullet")
        elif owner == "alien":
            return self.sprites.get("alien_bullet")
        else:
            return self.sprites.get("player_bullet")
    
    def get_sprite(self, name: str, size: tuple = (32, 32)) -> pygame.Surface:
        """Obtener un sprite, cargando SVG si existe o usando fallback procedural"""
        cache_key = f"{name}_{size[0]}x{size[1]}"
        
        if cache_key in self.sprites:
            return self.sprites[cache_key]
            
        # Intentar cargar SVG primero
        svg_path = f"assets/sprites/{name}.svg"
        sprite = self.load_svg(svg_path, size)
        
        if sprite is None:
            # Fallback a sprites procedurales
            sprite = self.create_procedural_sprite(name, size)
            
        self.sprites[cache_key] = sprite
        return sprite
    
    def load_svg(self, svg_path: str, size: tuple = None) -> Optional[pygame.Surface]:
        """Cargar un archivo SVG y convertirlo a Surface de Pygame"""
        if not SVG_SUPPORT:
            return None
            
        try:
            # Verificar si el archivo existe
            if not os.path.exists(svg_path):
                print(f"SVG no encontrado: {svg_path}")
                return None
                
            # Leer el archivo SVG
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
                
            # Convertir SVG a PNG usando cairosvg
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
            
            # Crear Surface desde PNG
            pil_image = Image.open(io.BytesIO(png_data))
            
            # Convertir PIL Image a pygame Surface
            mode = pil_image.mode
            size_img = pil_image.size
            raw = pil_image.tobytes()
            
            if mode == 'RGBA':
                surface = pygame.image.fromstring(raw, size_img, 'RGBA')
            else:
                surface = pygame.image.fromstring(raw, size_img, 'RGB')
                
            # Redimensionar si se especifica
            if size:
                surface = pygame.transform.scale(surface, size)
                
            return surface
            
        except Exception as e:
            print(f"Error cargando SVG {svg_path}: {e}")
            return None
    
    def create_procedural_sprite(self, name: str, size: tuple) -> pygame.Surface:
        """Crear sprites procedurales como fallback"""
        width, height = size
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if name == "player":
            # Nave espacial futurista
            # Cuerpo principal
            points = [
                (width // 2, height // 8),  # Punta
                (width // 4, height * 3 // 4),  # Izquierda
                (width // 2, height * 5 // 8),  # Centro
                (width * 3 // 4, height * 3 // 4)  # Derecha
            ]
            pygame.draw.polygon(surface, (74, 144, 226), points)
            pygame.draw.polygon(surface, (26, 92, 138), points, 2)
            
            # Cabina
            pygame.draw.ellipse(surface, (126, 211, 33), (width//2-4, height//3, 8, 12))
            pygame.draw.ellipse(surface, (65, 117, 5), (width//2-4, height//3, 8, 12), 1)
            
            # Motores
            pygame.draw.rect(surface, (255, 107, 107), (width//2-8, height*3//4, 4, 6))
            pygame.draw.rect(surface, (255, 107, 107), (width//2+4, height*3//4, 4, 6))
            
            # Detalles
            pygame.draw.circle(surface, (0, 184, 148), (width//2, height//2-2), 3)
            
        elif name == "alien":
            # Alien biomecánico
            # Cuerpo principal
            pygame.draw.ellipse(surface, (139, 69, 19), (0, height//3, width, height*2//3))
            # Caparazón
            pygame.draw.ellipse(surface, (160, 82, 45), (width//8, height//8, width*3//4, height*2//3))
            
            # Patas
            for i, x_pos in enumerate([width//4, width//3, width*2//3, width*3//4]):
                y_offset = 2 if i % 2 else 0
                pygame.draw.ellipse(surface, (101, 52, 33), (x_pos-2, height*3//4+y_offset, 4, 8))
            
            # Ojos
            pygame.draw.circle(surface, (255, 68, 68), (width//3, height//3), 4)
            pygame.draw.circle(surface, (255, 68, 68), (width*2//3, height//3), 4)
            pygame.draw.circle(surface, (0, 0, 0), (width//3, height//3), 2)
            pygame.draw.circle(surface, (0, 0, 0), (width*2//3, height//3), 2)
            
            # Brillos
            pygame.draw.circle(surface, (255, 255, 255), (width//3+1, height//3-1), 1)
            pygame.draw.circle(surface, (255, 255, 255), (width*2//3+1, height//3-1), 1)
            
            # Antenas
            pygame.draw.line(surface, (101, 52, 33), (width//3, height//8), (width//3-4, height//16), 2)
            pygame.draw.line(surface, (101, 52, 33), (width*2//3, height//8), (width*2//3+4, height//16), 2)
            pygame.draw.circle(surface, (255, 68, 68), (width//3-4, height//16), 1)
            pygame.draw.circle(surface, (255, 68, 68), (width*2//3+4, height//16), 1)
            
        elif name == "bullet_player":
            # Bala energética azul
            # Resplandor
            pygame.draw.ellipse(surface, (0, 255, 255, 128), (0, 0, width, height))
            # Núcleo
            pygame.draw.ellipse(surface, (0, 128, 255), (width//4, height//4, width//2, height//2))
            pygame.draw.ellipse(surface, (255, 255, 255), (width//3, height//3, width//3, height//3))
            
        elif name == "bullet_alien":
            # Bala ácida
            # Resplandor
            pygame.draw.ellipse(surface, (255, 255, 0, 128), (0, 0, width, height))
            # Núcleo
            pygame.draw.ellipse(surface, (255, 102, 0), (width//4, height//4, width//2, height//2))
            # Gotas
            pygame.draw.circle(surface, (255, 255, 0), (width//4, height*3//4), 1)
            pygame.draw.circle(surface, (255, 255, 0), (width*3//4, height*2//3), 1)
            
        elif name == "wall":
            # Muro futurista
            pygame.draw.rect(surface, (102, 102, 102), (0, 0, width, height))
            pygame.draw.rect(surface, (153, 153, 153), (2, 2, width-4, height-4))
            
            # Paneles
            pygame.draw.rect(surface, (85, 85, 85), (2, 2, width-4, height//2-2))
            pygame.draw.rect(surface, (85, 85, 85), (2, height//2+2, width-4, height//2-4))
            
            # Tornillos
            pygame.draw.circle(surface, (119, 119, 119), (6, 6), 1)
            pygame.draw.circle(surface, (119, 119, 119), (width-6, 6), 1)
            pygame.draw.circle(surface, (119, 119, 119), (6, height-6), 1)
            pygame.draw.circle(surface, (119, 119, 119), (width-6, height-6), 1)
            
            # Líneas divisorias
            pygame.draw.line(surface, (119, 119, 119), (0, height//2), (width, height//2), 1)
            pygame.draw.line(surface, (119, 119, 119), (width//2, 0), (width//2, height), 1)
            
        elif name == "floor":
            # Piso de base espacial
            pygame.draw.rect(surface, (42, 42, 42), (0, 0, width, height))
            
            # Patrón de rejilla
            for i in range(0, width, 8):
                pygame.draw.line(surface, (51, 51, 51), (i, 0), (i, height))
            for i in range(0, height, 8):
                pygame.draw.line(surface, (51, 51, 51), (0, i), (width, i))
                
            # Círculos tecnológicos
            pygame.draw.circle(surface, (0, 64, 128), (width//2, height//2), 8, 1)
            pygame.draw.circle(surface, (0, 64, 128), (width//2, height//2), 4, 1)
            
            # LEDs
            pygame.draw.rect(surface, (0, 255, 0), (2, 2, 2, 2))
            pygame.draw.rect(surface, (0, 255, 0), (width-4, 2, 2, 2))
            pygame.draw.rect(surface, (0, 255, 0), (2, height-4, 2, 2))
            pygame.draw.rect(surface, (0, 255, 0), (width-4, height-4, 2, 2))
            
        elif name == "health_icon":
            # Icono de salud
            pygame.draw.circle(surface, (0, 255, 0), (width//2, height//2), width//2-2)
            pygame.draw.circle(surface, (0, 68, 0), (width//2, height//2), width//2-2, 2)
            
            # Cruz
            pygame.draw.rect(surface, (255, 255, 255), (width//2-2, height//4+2, 4, height//2-4))
            pygame.draw.rect(surface, (255, 255, 255), (width//4+2, height//2-2, width//2-4, 4))
            
        elif name == "ammo_icon":
            # Icono de munición
            pygame.draw.circle(surface, (255, 215, 0), (width//2, height//2), width//2-2)
            pygame.draw.circle(surface, (184, 134, 11), (width//2, height//2), width//2-2, 2)
            
            # Bala
            pygame.draw.ellipse(surface, (192, 192, 192), (width//2-3, height//4, 6, height//2))
            pygame.draw.ellipse(surface, (255, 255, 255), (width//2-2, height//4, 4, height//3))
            pygame.draw.rect(surface, (205, 133, 63), (width//2-3, height*3//4, 6, height//6))
            
        else:
            # Sprite por defecto
            pygame.draw.rect(surface, (255, 0, 255), (0, 0, width, height))
            
        return surface
    
    def rotate_sprite(self, sprite: pygame.Surface, angle: float) -> pygame.Surface:
        """Rotar un sprite"""
        return pygame.transform.rotate(sprite, angle)
    
    def scale_sprite(self, sprite: pygame.Surface, scale: float) -> pygame.Surface:
        """Escalar un sprite"""
        new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
        return pygame.transform.scale(sprite, new_size)
    
    def clear_cache(self):
        """Limpiar caché de sprites"""
        self.sprites.clear()
        self.loaded_svgs.clear()
        
    def preload_sprites(self):
        """Precargar sprites comunes"""
        common_sprites = [
            ("player", (32, 32)),
            ("alien", (32, 32)),
            ("bullet_player", (8, 16)),
            ("bullet_alien", (8, 12)),
            ("wall", (32, 32)),
            ("floor", (32, 32)),
            ("health_icon", (24, 24)),
            ("ammo_icon", (24, 24))
        ]
        
        print("Precargando sprites...")
        for name, size in common_sprites:
            sprite = self.get_sprite(name, size)
            if sprite:
                print(f"  ✓ {name} ({size[0]}x{size[1]})")
            else:
                print(f"  ✗ Error cargando {name}")
                
        print(f"Sprites cargados: {len(self.sprites)}")
        print(f"Soporte SVG: {'Sí' if SVG_SUPPORT else 'No (usando sprites procedurales)'}")
    
    def add_sprite(self, name, sprite):
        """Agregar un sprite al manager"""
        self.sprites[name] = sprite
    
    def tint_sprite(self, sprite, color):
        """Aplicar tinte a un sprite"""
        tinted = sprite.copy()
        tinted.fill(color, special_flags=pygame.BLEND_MULT)
        return tinted 
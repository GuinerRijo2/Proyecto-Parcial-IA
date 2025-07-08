#!/usr/bin/env python3
"""
Alien Breed 92 SE - Juego desarrollado con Pygame
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]

Juego inspirado en Alien Breed 92 con vista isométrica donde el jugador
debe sobrevivir en una estación espacial llena de alienígenas.
"""

import pygame
import sys
import os

# Agregar el directorio scripts al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from scripts.game import Game
from scripts.settings import *

def main():
    """Función principal del juego"""
    pygame.init()
    pygame.mixer.init()
    
    # Configurar la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alien Breed 92 SE")
    
    # Inicializar el reloj
    clock = pygame.time.Clock()
    
    # Crear instancia del juego
    game = Game(screen)
    
    # Bucle principal
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time en segundos
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Actualizar juego
        game.update(dt)
        
        # Renderizar
        game.draw()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 
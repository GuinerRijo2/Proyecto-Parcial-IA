# Proyecto-parcial-IA

## Nombre: Guiner Rijo Martínez

## Matrícula: 21-SISN-2-035

## Proyecto: Alien Breed 92 SE


# Alien Breed 92 SE

Un clon del clásico juego Alien Breed 92 desarrollado en Python usando Pygame. El jugador debe sobrevivir en una estación espacial infestada de alienígenas utilizando armas y estrategia.

## Características

- **Gameplay Clásico**: Acción top-down inspirada en Alien Breed 92
- **Inteligencia Artificial Avanzada**: 
  - Árbol de Comportamiento implementado desde cero para enemigos
  - Algoritmo A* para pathfinding inteligente
- **Sistema de Controles Avanzado**: Teclado+Mouse y gamepad con apuntado independiente
- **Sistema de Audio**: Música de fondo y efectos de sonido
- **Gráficos**: Sprites personalizados con efectos visuales

## Requisitos del Sistema

- Python 3.7 o superior
- Pygame 2.5.2 o superior
- NumPy 1.24.3 o superior

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/GuinerRijo2/Proyecto-Parcial-IA

```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Cómo Jugar

1. Ejecuta el juego:
```bash
python main.py
```

2. **Controles** (Sistema de Apuntado Mejorado):
   
   **Teclado + Mouse:**
   - **WASD** o **Flechas**: Mover
   - **Mouse**: Apuntar (apunta hacia el cursor)
   - **Espacio**: Disparar
   - **ESC**: Pausa/Menú
   
   **Gamepad (Auto-detectado):**
   - **PS5 DualSense**: 
     - Stick izquierdo: Mover
     - Stick derecho: Apuntar
     - X (Cruz): Disparar
     - Options: Pausa
   - **Xbox Controller**: 
     - Stick izquierdo: Mover
     - Stick derecho: Apuntar
     - A: Disparar
     - Menu: Pausa
   
   **Sistema de Apuntado Inteligente:**
   - **Mouse**: Apunta hacia el cursor del mouse (indicador verde)
   - **Stick derecho**: Apunta en la dirección del stick (indicador azul)
   - **Movimiento**: Si no hay mouse/stick activo, apunta en dirección del movimiento
   - **Prioridad**: Mouse > Gamepad > Movimiento

3. **Objetivo**: Elimina todos los alienígenas para ganar el nivel

## Arquitectura del Proyecto

```
proyecto/
├── main.py                 # Punto de entrada principal
├── scripts/
│   ├── __init__.py
│   ├── settings.py         # Configuración del juego
│   ├── game.py            # Clase principal del juego
│   ├── menu.py            # Sistema de menús
│   ├── level.py           # Lógica del nivel
│   ├── player.py          # Jugador
│   ├── alien.py           # Enemigos alienígenas
│   ├── bullet.py          # Sistema de proyectiles
│   ├── a_star.py          # Algoritmo A* (implementación propia)
│   ├── behavior_tree.py   # Árbol de Comportamiento (implementación propia)
│   ├── input_handler.py   # Manejo de entrada
│   ├── audio_manager.py   # Sistema de audio
│   └── sprite_manager.py  # Manejo de sprites
├── assets/
│   ├── images/            # Sprites e imágenes
│   ├── sounds/            # Efectos de sonido
│   └── music/             # Música de fondo
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Inteligencia Artificial

### Árbol de Comportamiento
Los enemigos utilizan un árbol de comportamiento personalizado que incluye:
- **Patrullaje**: Movimiento automático cuando no hay amenazas
- **Detección**: Búsqueda activa del jugador
- **Persecución**: Seguimiento inteligente usando A*
- **Ataque**: Combate cuerpo a cuerpo y a distancia
- **Huida**: Retirada estratégica cuando la salud es baja

### Pathfinding A*
Implementación completa del algoritmo A* que permite:
- Navegación inteligente evitando obstáculos
- Suavizado de rutas para movimiento natural
- Recálculo dinámico según cambios en el entorno
- Optimización de rendimiento con actualización por intervalos

## Desarrollo

### Características Técnicas
- Implementación desde cero de A* y Árbol de Comportamiento
- **Sistema de entrada híbrido**: Soporte simultáneo para teclado y gamepad
  - Detección automática de mandos PS5, Xbox y genéricos
  - Mapeo específico por tipo de controlador
  - Priorización inteligente de entrada
  - Normalización de movimiento diagonal
- **Sistema de apuntado avanzado**: 
  - Apuntado independiente del movimiento
  - Soporte para mouse y stick derecho del gamepad
  - Indicadores visuales por tipo de control
  - Rotación suave y responsiva
- Sistema de audio sintético cuando no hay archivos de sonido
- Sprites procedurales como fallback
- Optimización de rendimiento para 60 FPS estables
- Sistema de cámara suave que sigue al jugador

### Requisitos del Proyecto
✅ Árbol de Comportamiento implementado desde cero  
✅ Algoritmo A* implementado desde cero  
✅ Soporte híbrido para gamepad y teclado  
✅ Sistema de audio (música y efectos)  
✅ Sprites y gráficos  
✅ Menú del juego  
✅ Sistema de reinicio  
✅ Estructura de proyecto organizada  
✅ Detección automática de tipos de mando  

## Licencia

Este proyecto es para fines educativos.

## Notas

- Los sonidos se generan sintéticamente si no se encuentran archivos de audio
- Los sprites se crean proceduralmente si no se encuentran imágenes
- El juego está optimizado para mantener 60 FPS consistentes
- Compatible con Windows, Linux y macOS 

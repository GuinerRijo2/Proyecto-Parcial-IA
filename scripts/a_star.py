"""
Implementación del algoritmo A* para pathfinding en Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

import heapq
import math
from .settings import *

class Node:
    """Nodo para el algoritmo A*"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g_cost = 0  # Costo desde el inicio
        self.h_cost = 0  # Heurística al objetivo
        self.f_cost = 0  # g_cost + h_cost
        self.parent = None
    
    def __lt__(self, other):
        """Comparación para el heap (prioridad por f_cost)"""
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        """Igualdad basada en posición"""
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        """Hash para usar en sets"""
        return hash((self.x, self.y))

class AStar:
    """Implementación del algoritmo A* para pathfinding"""
    
    def __init__(self, grid):
        """
        Inicializar A* con un grid
        grid: matriz 2D donde 0 = transitable, 1 = obstáculo
        """
        self.grid = grid
        self.width = len(grid[0]) if grid else 0
        self.height = len(grid) if grid else 0
        
        # Direcciones de movimiento (8 direcciones)
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Arriba-izq, Arriba, Arriba-der
            (0, -1),           (0, 1),   # Izquierda, Derecha
            (1, -1),  (1, 0),  (1, 1)    # Abajo-izq, Abajo, Abajo-der
        ]
        
        # Costos de movimiento (diagonal cuesta más)
        self.move_costs = [
            1.414, 1.0, 1.414,  # Diagonales cuestan √2
            1.0,        1.0,    # Cardinales cuestan 1
            1.414, 1.0, 1.414   # Diagonales cuestan √2
        ]
    
    def is_valid_position(self, x, y):
        """Verificar si una posición es válida y transitable"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y][x] == FLOOR_TILE
    
    def heuristic(self, node, goal):
        """Calcular la heurística (distancia euclidiana)"""
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        return math.sqrt(dx * dx + dy * dy)
    
    def get_neighbors(self, node):
        """Obtener vecinos válidos de un nodo"""
        neighbors = []
        
        for i, (dx, dy) in enumerate(self.directions):
            new_x = node.x + dx
            new_y = node.y + dy
            
            if self.is_valid_position(new_x, new_y):
                neighbor = Node(new_x, new_y)
                neighbor.g_cost = node.g_cost + self.move_costs[i]
                neighbors.append(neighbor)
        
        return neighbors
    
    def reconstruct_path(self, node):
        """Reconstruir el camino desde el nodo objetivo al inicio"""
        path = []
        current = node
        
        while current is not None:
            path.append((current.x, current.y))
            current = current.parent
        
        return path[::-1]  # Invertir para obtener camino desde inicio a objetivo
    
    def find_path(self, start_pos, goal_pos):
        """
        Encontrar camino desde start_pos hasta goal_pos
        Retorna una lista de tuplas (x, y) representando el camino
        """
        start_x, start_y = start_pos
        goal_x, goal_y = goal_pos
        
        # Verificar posiciones válidas
        if not self.is_valid_position(start_x, start_y):
            print(f"Posición de inicio inválida: {start_pos}")
            return []
        
        if not self.is_valid_position(goal_x, goal_y):
            print(f"Posición objetivo inválida: {goal_pos}")
            return []
        
        # Si ya estamos en el objetivo
        if start_x == goal_x and start_y == goal_y:
            return [start_pos]
        
        # Inicializar nodos
        start_node = Node(start_x, start_y)
        goal_node = Node(goal_x, goal_y)
        
        # Listas para A*
        open_list = []
        closed_set = set()
        
        # Agregar nodo inicial
        heapq.heappush(open_list, start_node)
        
        while open_list:
            # Obtener nodo con menor f_cost
            current = heapq.heappop(open_list)
            
            # Agregar a lista cerrada
            closed_set.add((current.x, current.y))
            
            # Verificar si llegamos al objetivo
            if current.x == goal_node.x and current.y == goal_node.y:
                return self.reconstruct_path(current)
            
            # Examinar vecinos
            for neighbor in self.get_neighbors(current):
                # Saltar si ya está en lista cerrada
                if (neighbor.x, neighbor.y) in closed_set:
                    continue
                
                # Calcular costos
                neighbor.h_cost = self.heuristic(neighbor, goal_node)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                neighbor.parent = current
                
                # Verificar si ya está en open_list con mejor costo
                in_open_list = False
                for open_node in open_list:
                    if (open_node.x == neighbor.x and 
                        open_node.y == neighbor.y and 
                        open_node.f_cost <= neighbor.f_cost):
                        in_open_list = True
                        break
                
                if not in_open_list:
                    heapq.heappush(open_list, neighbor)
        
        # No se encontró camino
        return []
    
    def smooth_path(self, path):
        """Suavizar el camino eliminando puntos innecesarios"""
        if len(path) <= 2:
            return path
        
        smoothed = [path[0]]
        
        i = 0
        while i < len(path) - 1:
            # Encontrar el punto más lejano al que podemos ir en línea recta
            for j in range(len(path) - 1, i, -1):
                if self.is_line_clear(path[i], path[j]):
                    smoothed.append(path[j])
                    i = j
                    break
            else:
                i += 1
        
        return smoothed
    
    def is_line_clear(self, start, end):
        """Verificar si hay línea clara entre dos puntos"""
        x0, y0 = start
        x1, y1 = end
        
        # Algoritmo de línea de Bresenham simplificado
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        x_step = 1 if x0 < x1 else -1
        y_step = 1 if y0 < y1 else -1
        
        error = dx - dy
        x, y = x0, y0
        
        while True:
            if not self.is_valid_position(x, y):
                return False
            
            if x == x1 and y == y1:
                break
            
            error2 = 2 * error
            
            if error2 > -dy:
                error -= dy
                x += x_step
            
            if error2 < dx:
                error += dx
                y += y_step
        
        return True 
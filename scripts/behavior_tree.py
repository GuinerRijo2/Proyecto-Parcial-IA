"""
Implementación de Árbol de Comportamiento para IA en Alien Breed 92 SE
Nombre: [Tu Nombre]
Matrícula: [Tu Matrícula]
"""

from enum import Enum
import math
import pygame
from .settings import *

class NodeStatus(Enum):
    """Estados posibles de un nodo del árbol de comportamiento"""
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"

class BehaviorNode:
    """Clase base para todos los nodos del árbol de comportamiento"""
    
    def __init__(self, name="Node"):
        self.name = name
        self.parent = None
        self.children = []
        self.status = NodeStatus.FAILURE
    
    def add_child(self, child):
        """Agregar un nodo hijo"""
        child.parent = self
        self.children.append(child)
        return self
    
    def tick(self, blackboard):
        """Ejecutar el nodo (debe ser implementado por las subclases)"""
        raise NotImplementedError("tick() debe ser implementado por las subclases")

class Selector(BehaviorNode):
    """Nodo Selector: ejecuta hijos hasta que uno tenga éxito"""
    
    def __init__(self, name="Selector"):
        super().__init__(name)
    
    def tick(self, blackboard):
        """Ejecutar selector (OR lógico)"""
        for child in self.children:
            status = child.tick(blackboard)
            
            if status == NodeStatus.SUCCESS:
                self.status = NodeStatus.SUCCESS
                return self.status
            elif status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status
        
        self.status = NodeStatus.FAILURE
        return self.status

class Sequence(BehaviorNode):
    """Nodo Secuencia: ejecuta hijos hasta que uno falle"""
    
    def __init__(self, name="Sequence"):
        super().__init__(name)
    
    def tick(self, blackboard):
        """Ejecutar secuencia (AND lógico)"""
        for child in self.children:
            status = child.tick(blackboard)
            
            if status == NodeStatus.FAILURE:
                self.status = NodeStatus.FAILURE
                return self.status
            elif status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status
        
        self.status = NodeStatus.SUCCESS
        return self.status

class Condition(BehaviorNode):
    """Nodo condición base"""
    
    def __init__(self, name="Condition", condition_func=None):
        super().__init__(name)
        self.condition_func = condition_func
    
    def tick(self, blackboard):
        """Evaluar condición"""
        if self.condition_func and self.condition_func(blackboard):
            self.status = NodeStatus.SUCCESS
        else:
            self.status = NodeStatus.FAILURE
        return self.status

class Action(BehaviorNode):
    """Nodo acción base"""
    
    def __init__(self, name="Action", action_func=None):
        super().__init__(name)
        self.action_func = action_func
    
    def tick(self, blackboard):
        """Ejecutar acción"""
        if self.action_func:
            result = self.action_func(blackboard)
            if result is None:
                self.status = NodeStatus.SUCCESS
            else:
                self.status = result
        else:
            self.status = NodeStatus.SUCCESS
        return self.status

class Blackboard:
    """Pizarra compartida para almacenar datos entre nodos"""
    
    def __init__(self):
        self.data = {}
    
    def set(self, key, value):
        """Establecer valor en la pizarra"""
        self.data[key] = value
    
    def get(self, key, default=None):
        """Obtener valor de la pizarra"""
        return self.data.get(key, default)
    
    def has(self, key):
        """Verificar si existe una clave"""
        return key in self.data

class AlienBehaviorTree:
    """Árbol de comportamiento específico para los aliens"""
    
    def __init__(self, alien):
        self.alien = alien
        self.blackboard = Blackboard()
        self.root = self.create_tree()
        
        # Inicializar pizarra
        self.blackboard.set('self', alien)
        self.blackboard.set('current_time', 0)
        self.blackboard.set('last_attack_time', 0)
    
    def create_tree(self):
        """Crear el árbol de comportamiento del alien"""
        root = Selector("Comportamiento Principal")
        
        # Secuencia de combate
        combat_sequence = Sequence("Combate")
        combat_sequence.add_child(Condition("Jugador Visible", self.player_in_sight))
        
        combat_actions = Selector("Acciones de Combate")
        
        # Ataque
        attack_sequence = Sequence("Ataque")
        attack_sequence.add_child(Condition("En Rango de Ataque", self.player_in_attack_range))
        attack_sequence.add_child(Action("Atacar", self.attack_player_action))
        
        # Persecución
        chase_sequence = Sequence("Persecución")
        chase_sequence.add_child(Condition("Hay Camino", self.has_path_to_player))
        chase_sequence.add_child(Action("Perseguir", self.chase_player_action))
        
        combat_actions.add_child(attack_sequence)
        combat_actions.add_child(chase_sequence)
        combat_sequence.add_child(combat_actions)
        
        # Secuencia de huida
        flee_sequence = Sequence("Huida")
        flee_sequence.add_child(Condition("Salud Baja", self.is_health_low))
        flee_sequence.add_child(Action("Huir", self.flee_action))
        
        # Agregar secuencias al selector principal
        root.add_child(combat_sequence)
        root.add_child(flee_sequence)
        root.add_child(Action("Patrullar", self.patrol_action))
        
        return root
    
    # Condiciones
    def player_in_sight(self, blackboard):
        """Verificar si el jugador está a la vista"""
        alien = blackboard.get('self')
        player = blackboard.get('player')
        
        if not alien or not player:
            return False
        
        dx = player.x - alien.x
        dy = player.y - alien.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance <= VISION_RANGE
    
    def player_in_attack_range(self, blackboard):
        """Verificar si el jugador está en rango de ataque"""
        alien = blackboard.get('self')
        player = blackboard.get('player')
        
        if not alien or not player:
            return False
        
        dx = player.x - alien.x
        dy = player.y - alien.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance <= ATTACK_RANGE
    
    def has_path_to_player(self, blackboard):
        """Verificar si hay un camino disponible al jugador"""
        path = blackboard.get('path_to_player')
        return path is not None and len(path) > 0
    
    def is_health_low(self, blackboard):
        """Verificar si la salud está baja"""
        alien = blackboard.get('self')
        if not alien:
            return False
        
        return hasattr(alien, 'health') and alien.health < alien.max_health * 0.3
    
    # Acciones
    def patrol_action(self, blackboard):
        """Acción de patrullaje"""
        alien = blackboard.get('self')
        if not alien:
            return NodeStatus.FAILURE
        
        patrol_points = blackboard.get('patrol_points', [])
        current_target = blackboard.get('current_patrol_target', 0)
        
        if not patrol_points:
            import random
            start_x, start_y = getattr(alien, 'start_x', alien.x), getattr(alien, 'start_y', alien.y)
            patrol_points = [
                (start_x + random.randint(-100, 100), start_y + random.randint(-100, 100))
                for _ in range(4)
            ]
            blackboard.set('patrol_points', patrol_points)
        
        target_x, target_y = patrol_points[current_target]
        
        dx = target_x - alien.x
        dy = target_y - alien.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < 20:
            current_target = (current_target + 1) % len(patrol_points)
            blackboard.set('current_patrol_target', current_target)
        
        if distance > 0:
            alien.vel_x = (dx / distance) * ALIEN_SPEED * 0.01
            alien.vel_y = (dy / distance) * ALIEN_SPEED * 0.01
        
        return NodeStatus.RUNNING
    
    def chase_player_action(self, blackboard):
        """Acción de perseguir al jugador"""
        alien = blackboard.get('self')
        player = blackboard.get('player')
        
        if not alien or not player:
            return NodeStatus.FAILURE
        
        path = blackboard.get('path_to_player')
        if not path or len(path) < 2:
            return NodeStatus.FAILURE
        
        next_point = path[1]
        target_x = next_point[0] * TILE_SIZE + TILE_SIZE // 2
        target_y = next_point[1] * TILE_SIZE + TILE_SIZE // 2
        
        dx = target_x - alien.x
        dy = target_y - alien.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            alien.vel_x = (dx / distance) * ALIEN_SPEED * 0.015
            alien.vel_y = (dy / distance) * ALIEN_SPEED * 0.015
        
        return NodeStatus.RUNNING
    
    def attack_player_action(self, blackboard):
        """Acción de atacar al jugador"""
        alien = blackboard.get('self')
        player = blackboard.get('player')
        
        if not alien or not player:
            return NodeStatus.FAILURE
        
        current_time = blackboard.get('current_time', 0)
        last_attack = blackboard.get('last_attack_time', 0)
        
        if current_time - last_attack >= 1.0:
            if hasattr(alien, 'shoot_at_player'):
                bullets = blackboard.get('bullets', [])
                audio_manager = blackboard.get('audio_manager')
                alien.shoot_at_player(player, bullets, audio_manager)
            blackboard.set('last_attack_time', current_time)
            return NodeStatus.SUCCESS
        
        return NodeStatus.RUNNING
    
    def flee_action(self, blackboard):
        """Acción de huir del jugador"""
        alien = blackboard.get('self')
        player = blackboard.get('player')
        
        if not alien or not player:
            return NodeStatus.FAILURE
        
        dx = alien.x - player.x
        dy = alien.y - player.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            alien.vel_x = (dx / distance) * ALIEN_SPEED * 0.02
            alien.vel_y = (dy / distance) * ALIEN_SPEED * 0.02
        
        return NodeStatus.RUNNING
    
    def update(self, dt, player, level_map, bullets, audio_manager):
        """Actualizar el árbol de comportamiento"""
        current_time = pygame.time.get_ticks() / 1000.0
        
        self.blackboard.set('player', player)
        self.blackboard.set('current_time', current_time)
        self.blackboard.set('level_map', level_map)
        self.blackboard.set('bullets', bullets)
        self.blackboard.set('audio_manager', audio_manager)
        
        return self.root.tick(self.blackboard)
    
    def set_path_to_player(self, path):
        """Establecer camino calculado hacia el jugador"""
        self.blackboard.set('path_to_player', path) 
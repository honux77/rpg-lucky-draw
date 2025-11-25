"""RPG Character class for the lucky draw battle system."""

import random
from typing import Optional


class Character:
    """RPG Character with combat stats and battle capabilities."""
    
    def __init__(self, name: str, level: Optional[int] = None):
        """
        Initialize a character with random or specified stats.
        
        Args:
            name: Character name (typically username from Naver comments)
            level: Optional fixed level, otherwise random 1-10
        """
        self.name = name
        self.level = level if level is not None else random.randint(1, 10)
        
        # Base stats scaled by level
        base_hp = random.randint(50, 100)
        base_attack = random.randint(10, 20)
        base_defense = random.randint(5, 15)
        base_speed = random.randint(5, 15)
        
        self.max_hp = base_hp + (self.level * 10)
        self.hp = self.max_hp
        self.attack = base_attack + (self.level * 2)
        self.defense = base_defense + self.level
        self.speed = base_speed + self.level
        
        self.is_alive = True
    
    def take_damage(self, damage: int) -> int:
        """
        Apply damage to character, reducing by defense.
        
        Args:
            damage: Raw damage amount
            
        Returns:
            Actual damage taken after defense calculation
        """
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
        
        return actual_damage
    
    def attack_target(self, target: 'Character') -> dict:
        """
        Attack another character.
        
        Args:
            target: Target character to attack
            
        Returns:
            Dictionary with attack details (damage, critical hit, etc.)
        """
        # Critical hit chance (20%)
        is_critical = random.random() < 0.2
        damage = self.attack
        
        if is_critical:
            damage = int(damage * 1.5)
        
        actual_damage = target.take_damage(damage)
        
        return {
            'attacker': self.name,
            'target': target.name,
            'damage': damage,
            'actual_damage': actual_damage,
            'critical': is_critical,
            'target_hp': target.hp,
            'target_alive': target.is_alive
        }
    
    def __str__(self) -> str:
        """String representation of character."""
        return f"{self.name} (Lv.{self.level}) - HP: {self.hp}/{self.max_hp}, ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed}"
    
    def __repr__(self) -> str:
        """Developer representation of character."""
        return f"Character(name='{self.name}', level={self.level}, hp={self.hp}/{self.max_hp})"

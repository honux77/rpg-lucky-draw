"""Battle system for RPG character combat."""

import random
from typing import List, Optional
from character import Character


class Battle:
    """Manages combat between two characters."""
    
    def __init__(self, char1: Character, char2: Character, verbose: bool = True):
        """
        Initialize a battle between two characters.
        
        Args:
            char1: First character
            char2: Second character
            verbose: Whether to print battle logs
        """
        self.char1 = char1
        self.char2 = char2
        self.verbose = verbose
        self.battle_log = []
    
    def _log(self, message: str):
        """Add message to battle log and optionally print."""
        self.battle_log.append(message)
        if self.verbose:
            print(message)
    
    def fight(self) -> Character:
        """
        Execute the battle until one character is defeated.
        
        Returns:
            The winning character
        """
        self._log(f"\n⚔️  전투 시작! {self.char1.name} vs {self.char2.name}")
        self._log(f"  {self.char1}")
        self._log(f"  {self.char2}")
        self._log("")
        
        round_num = 1
        
        while self.char1.is_alive and self.char2.is_alive:
            self._log(f"--- Round {round_num} ---")
            
            # Determine turn order by speed (higher speed attacks first)
            if self.char1.speed >= self.char2.speed:
                first, second = self.char1, self.char2
            else:
                first, second = self.char2, self.char1
            
            # First attacker's turn
            if first.is_alive:
                result = first.attack_target(second)
                self._log(self._format_attack(result))
                
                if not second.is_alive:
                    break
            
            # Second attacker's turn
            if second.is_alive:
                result = second.attack_target(first)
                self._log(self._format_attack(result))
            
            self._log("")
            round_num += 1
        
        winner = self.char1 if self.char1.is_alive else self.char2
        self._log(f"🏆 승자: {winner.name}!")
        self._log("")
        
        return winner
    
    def _format_attack(self, result: dict) -> str:
        """Format an attack result as a readable string."""
        crit_text = " 💥 크리티컬!" if result['critical'] else ""
        return (f"  {result['attacker']}의 공격! "
                f"{result['target']}에게 {result['actual_damage']} 데미지!{crit_text} "
                f"(남은 HP: {result['target_hp']})")


class Tournament:
    """Manages a tournament-style battle royale."""
    
    def __init__(self, characters: List[Character], verbose: bool = True):
        """
        Initialize a tournament with multiple characters.
        
        Args:
            characters: List of characters to compete
            verbose: Whether to print battle logs
        """
        self.characters = characters.copy()
        self.verbose = verbose
    
    def run(self) -> Character:
        """
        Run the tournament until one character remains.
        
        Note: Characters carry their damage between rounds (HP is not reset),
        creating a battle royale style where surviving tough battles has consequences.
        Characters receiving byes maintain their HP advantage.
        
        Returns:
            The tournament champion
        """
        print(f"\n🎮 토너먼트 시작! 총 {len(self.characters)}명의 참가자")
        print("=" * 60)
        
        for i, char in enumerate(self.characters, 1):
            print(f"{i}. {char}")
        
        round_num = 1
        contestants = self.characters.copy()
        
        while len(contestants) > 1:
            print(f"\n{'=' * 60}")
            print(f"🏁 토너먼트 라운드 {round_num} - {len(contestants)}명 남음")
            print("=" * 60)
            
            # Shuffle for random matchups
            random.shuffle(contestants)
            
            winners = []
            
            # Pair up contestants
            for i in range(0, len(contestants), 2):
                if i + 1 < len(contestants):
                    # Normal battle between two characters
                    battle = Battle(contestants[i], contestants[i + 1], self.verbose)
                    winner = battle.fight()
                    winners.append(winner)
                else:
                    # Odd number: last character gets a bye
                    bye_char = contestants[i]
                    print(f"\n✨ {bye_char.name}는 부전승으로 다음 라운드 진출!")
                    winners.append(bye_char)
            
            contestants = winners
            round_num += 1
        
        champion = contestants[0]
        print(f"\n{'=' * 60}")
        print(f"👑 최종 우승자: {champion.name}! (남은 HP: {champion.hp}/{champion.max_hp})")
        print("=" * 60)
        
        return champion

#!/usr/bin/env python3
"""Example usage of the RPG Lucky Draw library."""

from naver_fetcher import NaverCommentFetcher
from character import Character
from battle import Battle, Tournament


def example_direct_battle():
    """Example: Direct 1v1 battle."""
    print("=" * 60)
    print("예제 1: 1:1 직접 대결")
    print("=" * 60)
    
    # Create two characters
    char1 = Character("용사김철수", level=5)
    char2 = Character("마법사이영희", level=5)
    
    # Run battle
    battle = Battle(char1, char2)
    winner = battle.fight()
    
    print(f"\n최종 승자: {winner.name}\n")


def example_tournament():
    """Example: Tournament with multiple characters."""
    print("=" * 60)
    print("예제 2: 토너먼트 (8명)")
    print("=" * 60)
    
    # Create characters from mock data
    fetcher = NaverCommentFetcher()
    usernames = fetcher.fetch_from_mock_data(8)
    
    characters = [Character(name) for name in usernames]
    
    # Run tournament
    tournament = Tournament(characters, verbose=False)
    champion = tournament.run()
    
    print(f"\n최종 승자: {champion.name}\n")


def example_custom_characters():
    """Example: Custom characters with specific stats."""
    print("=" * 60)
    print("예제 3: 커스텀 캐릭터 생성")
    print("=" * 60)
    
    # Create characters with fixed levels
    characters = [
        Character("전설의 용사", level=10),
        Character("초보 모험가", level=1),
        Character("중급 전사", level=5),
        Character("고급 마법사", level=8),
    ]
    
    print("\n캐릭터 정보:")
    for char in characters:
        print(f"  {char}")
    
    # Run tournament
    tournament = Tournament(characters, verbose=True)
    champion = tournament.run()


if __name__ == '__main__':
    example_direct_battle()
    input("\nPress Enter to continue to next example...\n")
    
    example_tournament()
    input("\nPress Enter to continue to next example...\n")
    
    example_custom_characters()

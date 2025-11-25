#!/usr/bin/env python3
"""RPG Lucky Draw - Main application."""

import argparse
import sys
from typing import List

from naver_fetcher import NaverCommentFetcher
from character import Character
from battle import Tournament


def create_characters_from_users(usernames: List[str]) -> List[Character]:
    """
    Create RPG characters from usernames.
    
    Args:
        usernames: List of usernames
        
    Returns:
        List of Character objects
    """
    print(f"\n⚡ {len(usernames)}명의 사용자를 RPG 캐릭터로 변환 중...")
    characters = [Character(name) for name in usernames]
    print("✅ 캐릭터 생성 완료!\n")
    return characters


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='RPG 스타일 랜덤 뽑기 - 네이버 댓글 사용자들의 전투 토너먼트',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 네이버 URL에서 댓글 추출 (실제 사용 시):
  python main.py --url "https://blog.naver.com/example/123456"
  
  # 목 데이터로 테스트:
  python main.py --mock 8
  
  # 목 데이터로 조용히 실행:
  python main.py --mock 4 --quiet
        """
    )
    
    parser.add_argument(
        '--url',
        type=str,
        help='네이버 블로그/카페 게시글 URL'
    )
    
    parser.add_argument(
        '--mock',
        type=int,
        metavar='N',
        help='목(mock) 데이터 사용 (N명의 테스트 사용자 생성)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='전투 상세 로그를 출력하지 않음 (결과만 표시)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.url and args.mock is None:
        parser.print_help()
        print("\n❌ 오류: --url 또는 --mock 옵션 중 하나를 지정해야 합니다.")
        sys.exit(1)
    
    if args.url and args.mock is not None:
        print("❌ 오류: --url과 --mock은 동시에 사용할 수 없습니다.")
        sys.exit(1)
    
    # Initialize fetcher
    fetcher = NaverCommentFetcher()
    
    # Fetch usernames
    print("=" * 60)
    print("🎮 RPG Lucky Draw - 댓글 사용자 배틀 로얄")
    print("=" * 60)
    
    if args.mock is not None:
        if args.mock < 2:
            print("❌ 오류: 최소 2명의 사용자가 필요합니다.")
            sys.exit(1)
        
        print(f"\n📋 목(mock) 데이터로 {args.mock}명의 테스트 사용자 생성 중...")
        usernames = fetcher.fetch_from_mock_data(args.mock)
    else:
        print(f"\n📋 네이버 URL에서 댓글 수집 중...")
        print(f"   URL: {args.url}")
        usernames = fetcher.fetch_comments(args.url)
    
    if not usernames:
        print("❌ 오류: 사용자를 찾을 수 없습니다.")
        sys.exit(1)
    
    if len(usernames) < 2:
        print(f"❌ 오류: 최소 2명의 사용자가 필요합니다. (현재: {len(usernames)}명)")
        sys.exit(1)
    
    print(f"✅ 총 {len(usernames)}명의 사용자 발견!")
    print("\n참가자 목록:")
    for i, username in enumerate(usernames, 1):
        print(f"  {i}. {username}")
    
    # Create characters
    characters = create_characters_from_users(usernames)
    
    # Run tournament
    tournament = Tournament(characters, verbose=not args.quiet)
    champion = tournament.run()
    
    print(f"\n🎉 최종 승자는 {champion.name}님 입니다! 축하합니다! 🎉")
    print()


if __name__ == '__main__':
    main()

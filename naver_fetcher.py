"""Naver comment fetcher for extracting usernames from blog/cafe posts."""

import requests
from bs4 import BeautifulSoup
from typing import List, Set
import re


class NaverCommentFetcher:
    """Fetches comments from Naver blog/cafe posts."""
    
    def __init__(self):
        """Initialize the fetcher with appropriate headers."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_comments(self, url: str) -> List[str]:
        """
        Fetch comment usernames from a Naver post URL.
        
        Args:
            url: Naver blog/cafe post URL
            
        Returns:
            List of unique usernames who commented
            
        Note:
            Due to Naver's iframe structure and API requirements, this is a 
            simplified implementation. For production use, you would need to:
            1. Handle Naver's API authentication
            2. Parse iframe content
            3. Handle dynamic content loaded via JavaScript
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            usernames = set()
            
            # Try to find comment sections with various selectors
            # Note: Naver's actual structure may vary and require API access
            comment_selectors = [
                '.comment_nick_info',
                '.ment_nick',
                '.comment_nickname',
                '.nick_name',
                'span.nick',
            ]
            
            for selector in comment_selectors:
                elements = soup.select(selector)
                for elem in elements:
                    username = elem.get_text(strip=True)
                    if username:
                        usernames.add(username)
            
            # Also try finding in script tags for dynamically loaded content
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Look for patterns like "userName":"something"
                    matches = re.findall(r'"userName"\s*:\s*"([^"]+)"', script.string)
                    usernames.update(matches)
                    
                    # Also look for "nickname" patterns
                    matches = re.findall(r'"nickname"\s*:\s*"([^"]+)"', script.string)
                    usernames.update(matches)
            
            result = sorted(list(usernames))
            
            if not result:
                print("⚠️  경고: 댓글을 찾을 수 없습니다. URL과 네이버 설정을 확인해주세요.")
                print("   (네이버 블로그/카페는 iframe과 API를 사용하여 실제 구현 시 추가 작업이 필요합니다)")
            
            return result
            
        except requests.RequestException as e:
            print(f"❌ 오류: URL 접근 실패 - {e}")
            return []
    
    def fetch_from_mock_data(self, num_users: int = 8) -> List[str]:
        """
        Generate mock usernames for testing purposes.
        
        Args:
            num_users: Number of mock users to generate
            
        Returns:
            List of mock usernames
        """
        mock_names = [
            "용사김철수", "마법사이영희", "전사박민수", "궁수최지은",
            "도적정민호", "성기사강서연", "암살자윤재현", "사제임수진",
            "팔라딘송하은", "흑마법사권도현", "드루이드장예린", "광전사한지우",
            "검술사조현우", "소환사신다은", "음유시인배준호", "연금술사홍서아"
        ]
        
        return mock_names[:min(num_users, len(mock_names))]

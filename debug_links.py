#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
링크 수집 디버그 - 어떤 링크들이 발견되는지 확인
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

query = "육아"
url = f"https://search.naver.com/search.naver?where=article&query={quote(query)}&start=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("="*60)
print(f"링크 수집 디버그: '{query}'")
print("="*60)

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"\n응답 코드: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 모든 링크 찾기
    all_links = soup.find_all('a', href=True)
    print(f"전체 링크 개수: {len(all_links)}개")

    # cafe.naver.com 링크만 필터링
    cafe_links = []
    for link in all_links:
        href = link.get('href', '')
        if 'cafe.naver.com' in href:
            text = link.get_text(strip=True)
            cafe_links.append({
                'text': text[:50] if text else '(텍스트 없음)',
                'href': href[:100]
            })

    print(f"\n카페 링크 개수: {len(cafe_links)}개")
    print("\n" + "="*60)
    print("카페 링크 상세:")
    print("="*60)

    for idx, link in enumerate(cafe_links[:10], 1):
        print(f"\n[{idx}]")
        print(f"  텍스트: {link['text']}")
        print(f"  URL: {link['href']}")

        # URL 패턴 분석
        href = link['href']
        if '/ArticleRead.nhn' in href:
            print(f"  패턴: ArticleRead.nhn ✓")
        elif '/ArticleRead.naver' in href:
            print(f"  패턴: ArticleRead.naver ✓")
        elif 'ArticleList' in href:
            print(f"  패턴: ArticleList (목록)")
        else:
            print(f"  패턴: 기타")

    if len(cafe_links) == 0:
        print("\n⚠️  카페 링크가 하나도 없습니다!")
        print("혹시 네트워크 환경이나 지역 제한이 있을 수 있습니다.")

except Exception as e:
    print(f"\n오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("디버그 완료")
print("="*60)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
링크 수집 상세 디버그 - URL 형식 확인
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
print(f"링크 상세 디버그: '{query}'")
print("="*60)

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"\n응답 코드: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 모든 링크 찾기
    all_links = soup.find_all('a', href=True)

    # cafe.naver.com 링크만 필터링
    cafe_links = []
    for link in all_links:
        href = link.get('href', '')
        if 'cafe.naver.com' in href:
            text = link.get_text(strip=True)
            cafe_links.append({
                'text': text,
                'href': href
            })

    print(f"\n카페 링크 개수: {len(cafe_links)}개")
    print("\n" + "="*60)
    print("카페 링크 상세 (처음 10개):")
    print("="*60)

    for idx, link in enumerate(cafe_links[:10], 1):
        print(f"\n[{idx}]")
        print(f"텍스트: {link['text'][:50]}")
        print(f"원본 URL: {link['href']}")

        # URL 분석
        href = link['href']
        if href.startswith('http'):
            print("  → 절대 경로 URL ✓")
        elif href.startswith('#'):
            print("  → 해시(#) 링크 (JavaScript 필요)")
        elif href.startswith('/'):
            print("  → 상대 경로 (base URL 필요)")
        elif href.startswith('about:'):
            print("  → about:blank (무효한 링크)")
        else:
            print(f"  → 기타 형식: {href[:50]}")

except Exception as e:
    print(f"\n오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("디버그 완료")
print("="*60)

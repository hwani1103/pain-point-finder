#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모바일 카페 URL 테스트 - 빠른 확인
"""

import requests
from bs4 import BeautifulSoup

# PC URL → 모바일 URL 변환
pc_url = "https://cafe.naver.com/remonterrace/34281342"
mobile_url = pc_url.replace('cafe.naver.com', 'm.cafe.naver.com')

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}

print("="*60)
print("모바일 카페 URL 테스트")
print("="*60)
print(f"\nPC URL: {pc_url}")
print(f"모바일 URL: {mobile_url}")

try:
    response = requests.get(mobile_url, headers=headers, timeout=10)
    print(f"\n응답 코드: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 모바일 카페 본문 셀렉터 시도
    selectors = [
        'div.post-view',
        'div.content-wrap',
        'div[class*="article"]',
        'div[class*="post"]',
        'div[class*="content"]',
    ]

    print("\n셀렉터 테스트:")
    found = False

    for sel in selectors:
        elem = soup.select_one(sel)
        if elem:
            text = elem.get_text(strip=True)
            if len(text) > 50:
                print(f"\n✓ {sel} - {len(text)}자")
                print(f"내용: {text[:200]}...")
                found = True
                break

    if not found:
        print("\n✗ 적합한 셀렉터 없음")
        print("\n전체 텍스트 (처음 300자):")
        print(soup.get_text(strip=True)[:300])

except Exception as e:
    print(f"\n오류: {e}")

print("\n" + "="*60)

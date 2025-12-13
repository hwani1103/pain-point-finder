#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
디시인사이드 빠른 테스트 - 여러 갤러리 시도
"""

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 인기 갤러리들
galleries = [
    ('baseball_new11', '국내야구'),
    ('stock', '주식'),
    ('dcbest', 'DCbest'),
]

print("="*60)
print("디시인사이드 빠른 테스트")
print("="*60)

for gall_id, name in galleries:
    print(f"\n[{name} 갤러리]")
    url = f"https://gall.dcinside.com/board/lists/?id={gall_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 게시글 찾기
        posts = soup.select('tr.ub-content')

        print(f"  게시글: {len(posts)}개")

        if len(posts) > 0:
            # 첫 게시글
            title_elem = posts[0].select_one('td.gall_tit a')
            if title_elem:
                title = title_elem.get_text(strip=True)
                print(f"  ✓ 제목: {title[:40]}...")
                print(f"\n✅ 작동함! 이 갤러리 사용 가능")
                break
        else:
            # 다른 셀렉터 시도
            all_text = soup.get_text(strip=True)
            if len(all_text) > 100:
                print(f"  텍스트: {all_text[:100]}...")

    except Exception as e:
        print(f"  오류: {e}")

print("\n" + "="*60)

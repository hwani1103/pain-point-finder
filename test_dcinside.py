#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
디시인사이드 크롤링 테스트 - 빠른 확인
"""

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("="*60)
print("디시인사이드 크롤링 테스트")
print("="*60)

# 테스트: 육아 갤러리
gallery_id = "parenting"  # 육아 갤러리
url = f"https://gall.dcinside.com/board/lists/?id={gallery_id}"

print(f"\n테스트 갤러리: {gallery_id}")
print(f"URL: {url}")

try:
    # 1. 갤러리 목록 가져오기
    print("\n[1단계] 갤러리 목록 가져오기...")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"응답 코드: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 게시글 목록 찾기
    posts = soup.select('tr.ub-content')
    print(f"발견된 게시글: {len(posts)}개")

    if len(posts) > 0:
        # 첫 번째 게시글 정보
        first_post = posts[0]

        # 제목과 링크
        title_elem = first_post.select_one('td.gall_tit a')
        if title_elem:
            title = title_elem.get_text(strip=True)
            href = title_elem.get('href', '')

            print(f"\n✓ 첫 번째 게시글:")
            print(f"  제목: {title}")
            print(f"  링크: {href[:100]}...")

            # 2. 게시글 방문
            if href.startswith('/'):
                post_url = f"https://gall.dcinside.com{href}"
            else:
                post_url = href

            print(f"\n[2단계] 게시글 방문...")
            print(f"  URL: {post_url[:100]}...")

            response = requests.get(post_url, headers=headers, timeout=10)
            print(f"  응답 코드: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')

            # 본문 추출 시도
            print(f"\n[3단계] 본문 추출...")

            selectors = [
                ('div.write_div', '게시글 본문'),
                ('div.writing_view_box', '본문 박스'),
                ('div[class*="write"]', 'write 클래스'),
            ]

            for selector, desc in selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    if len(text) > 20:
                        print(f"\n✓ {selector} ({desc})")
                        print(f"  텍스트 길이: {len(text)}자")
                        print(f"  내용: {text[:200]}...")

                        # Pain Point 키워드 확인
                        keywords = ['힘들', '어렵', '불편', '짜증', 'ㅠㅠ', 'ㅜㅜ']
                        found = [k for k in keywords if k in text]
                        if found:
                            print(f"  ✓ Pain Point 키워드 발견: {', '.join(found)}")

                        print("\n✅ 디시인사이드 크롤링 가능!")
                        break
            else:
                print("\n✗ 본문 추출 실패")
                print("전체 텍스트 (처음 300자):")
                print(soup.get_text(strip=True)[:300])
        else:
            print("\n✗ 게시글 링크를 찾지 못함")
    else:
        print("\n✗ 게시글 목록이 비어있음")
        print("\n전체 HTML (처음 500자):")
        print(soup.get_text(strip=True)[:500])

except Exception as e:
    print(f"\n오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("테스트 완료!")
print("="*60)

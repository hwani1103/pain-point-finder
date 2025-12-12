#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
디버그용 크롤러 - 무엇이 파싱되는지 확인
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def debug_naver_search(query):
    """네이버 검색 결과 디버깅"""
    print(f"\n{'='*60}")
    print(f"디버그: '{query}' 검색")
    print(f"{'='*60}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = f"https://search.naver.com/search.naver?where=blog&query={quote(query)}&start=1"
    print(f"\n요청 URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"응답 코드: {response.status_code}")
        print(f"응답 크기: {len(response.text)} bytes")

        soup = BeautifulSoup(response.text, 'html.parser')

        # 여러 가지 셀렉터 시도
        selectors = [
            'div.view_wrap',
            'li.bx',
            'div.total_wrap',
            'div.api_subject_bx',
            'div.detail_box',
            'div.sp_blog',
            'div[class*="blog"]',
            'div[class*="api"]',
            'li[class*="bx"]'
        ]

        print(f"\n{'='*60}")
        print("셀렉터 테스트 결과:")
        print(f"{'='*60}")

        for selector in selectors:
            items = soup.select(selector)
            print(f"{selector:30s} → {len(items):3d}개 발견")

            if len(items) > 0 and len(items) < 50:  # 너무 많으면 스킵
                # 첫 번째 항목의 구조 출력
                print(f"  첫 항목 클래스: {items[0].get('class', 'N/A')}")

                # 제목 찾기 시도
                title_selectors = ['a.title_link', 'a.api_txt_lines', 'a.link_tit', 'a']
                for ts in title_selectors:
                    title = items[0].select_one(ts)
                    if title:
                        print(f"  제목 발견 ({ts}): {title.get_text(strip=True)[:50]}...")
                        break

        # HTML 일부 저장 (디버깅용)
        print(f"\n{'='*60}")
        print("HTML 샘플 저장 중...")
        with open('debug_naver_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✓ debug_naver_response.html 파일로 저장됨")
        print(f"{'='*60}")

        # 모든 링크 출력
        all_links = soup.find_all('a', href=True)
        blog_links = [link for link in all_links if 'blog.naver.com' in link.get('href', '')]
        print(f"\n발견된 블로그 링크 수: {len(blog_links)}개")

        if blog_links:
            print("\n처음 5개 블로그 링크:")
            for i, link in enumerate(blog_links[:5], 1):
                print(f"  {i}. {link.get_text(strip=True)[:50]}...")
                print(f"     URL: {link.get('href')}")

    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("🔍 네이버 블로그 검색 디버거")
    print("="*60)

    query = input("\n디버그할 검색어 입력 (Enter=일상): ").strip() or "일상"

    debug_naver_search(query)

    print("\n" + "="*60)
    print("✅ 디버깅 완료!")
    print("debug_naver_response.html 파일을 확인해보세요.")
    print("="*60)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카페 검색 디버그 도구
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def debug_cafe_search(query):
    """카페 검색 결과 디버깅"""
    print(f"\n{'='*60}")
    print(f"디버그: '{query}' 카페 검색")
    print(f"{'='*60}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # site:cafe.naver.com 검색
    search_query = f"site:cafe.naver.com {query}"
    url = f"https://search.naver.com/search.naver?where=web&query={quote(search_query)}&start=1"

    print(f"\n요청 URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"응답 코드: {response.status_code}")
        print(f"응답 크기: {len(response.text)} bytes")

        soup = BeautifulSoup(response.text, 'html.parser')

        # 여러 가지 셀렉터 시도
        selectors = [
            'div.api_subject_bx',
            'div.total_wrap',
            'li.bx',
            'div.source_box',
            'div.web_cont',
            'li.web_item',
            'div[class*="result"]',
            'div[class*="api"]',
            'a[href*="cafe.naver"]'
        ]

        print(f"\n{'='*60}")
        print("셀렉터 테스트 결과:")
        print(f"{'='*60}")

        for selector in selectors:
            items = soup.select(selector)
            print(f"{selector:30s} → {len(items):3d}개 발견")

            if 0 < len(items) < 50 and 'cafe.naver' in str(items[0]):
                # 카페 관련 항목만 출력
                print(f"  ✓ 카페 링크 포함!")
                print(f"  첫 항목 클래스: {items[0].get('class', 'N/A')}")

                # 텍스트 추출
                text = items[0].get_text(strip=True)[:100]
                print(f"  텍스트: {text}...")

        # 모든 카페 링크 찾기
        all_links = soup.find_all('a', href=True)
        cafe_links = [link for link in all_links if 'cafe.naver.com' in link.get('href', '')]

        print(f"\n{'='*60}")
        print(f"발견된 카페 링크 수: {len(cafe_links)}개")
        print(f"{'='*60}")

        if cafe_links:
            print("\n처음 5개 카페 링크:")
            for i, link in enumerate(cafe_links[:5], 1):
                print(f"\n  {i}. 텍스트: {link.get_text(strip=True)[:50]}...")
                print(f"     URL: {link.get('href')[:80]}...")

                # 부모 요소 확인
                parent = link.parent
                if parent:
                    print(f"     부모 태그: {parent.name}")
                    print(f"     부모 클래스: {parent.get('class', 'N/A')}")

        # HTML 저장
        print(f"\n{'='*60}")
        print("HTML 샘플 저장 중...")
        with open('debug_cafe_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✓ debug_cafe_response.html 파일로 저장됨")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("🔍 네이버 카페 검색 디버거")
    print("="*60)

    query = input("\n디버그할 검색어 입력 (Enter=육아): ").strip() or "육아"

    debug_cafe_search(query)

    print("\n" + "="*60)
    print("✅ 디버깅 완료!")
    print("debug_cafe_response.html 파일을 확인해보세요.")
    print("="*60)

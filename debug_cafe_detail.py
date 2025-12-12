#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카페 검색 상세 디버그 - 실제 추출되는 내용 확인
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def debug_cafe_detail(query):
    """카페 검색 결과에서 실제 추출되는 내용 확인"""
    print(f"\n{'='*60}")
    print(f"상세 디버그: '{query}' 카페 검색")
    print(f"{'='*60}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = f"https://search.naver.com/search.naver?where=article&query={quote(query)}&start=1"
    print(f"\n요청 URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 카페 게시글 찾기
        cafe_items = soup.select('div.api_subject_bx')
        print(f"\n발견된 게시글: {len(cafe_items)}개")

        print(f"\n{'='*60}")
        print("처음 3개 게시글 상세 분석:")
        print(f"{'='*60}")

        for idx, item in enumerate(cafe_items[:3], 1):
            print(f"\n[게시글 {idx}]")
            print("-" * 60)

            # 제목 추출 시도
            print("\n[제목 추출 시도]")
            title_selectors = [
                'a.api_txt_lines',
                'a.title_link',
                'a.sub_txt',
                'a[href*="cafe.naver"]',
                'a[href*="blog.naver"]',
                'a'
            ]

            title = None
            link = None
            for sel in title_selectors:
                elem = item.select_one(sel)
                if elem:
                    title = elem.get_text(strip=True)
                    link = elem.get('href', '')
                    print(f"  ✓ {sel}: {title[:50]}...")
                    print(f"    링크: {link[:80]}...")
                    break

            # 본문 추출 시도
            print("\n[본문 추출 시도]")
            content_selectors = [
                'dd.api_txt_lines',
                'div.dsc_link',
                'dd.sh_blog_passage',
                'div.api_txt',
                'dd',
                'div.dsc'
            ]

            content = None
            for sel in content_selectors:
                elem = item.select_one(sel)
                if elem:
                    content = elem.get_text(strip=True)
                    print(f"  ✓ {sel}: {content[:100]}...")
                    break

            # 키워드 체크
            if title or content:
                full_text = f"{title or ''} {content or ''}"
                print(f"\n[전체 텍스트]")
                print(f"  {full_text[:200]}...")

                # Pain Point 키워드 찾기
                pain_keywords = ['불편', '힘들', '어려', '짜증', 'ㅠㅠ', '진짜', '너무']
                found_keywords = [k for k in pain_keywords if k in full_text]

                if found_keywords:
                    print(f"\n  ✓ Pain Point 키워드 발견: {', '.join(found_keywords)}")
                else:
                    print(f"\n  ✗ Pain Point 키워드 없음")
            else:
                print(f"\n  ✗ 제목이나 본문을 추출하지 못했습니다!")

            # HTML 구조 출력
            print(f"\n[HTML 구조]")
            print(f"  태그: {item.name}")
            print(f"  클래스: {item.get('class', 'N/A')}")
            print(f"  자식 요소: {len(item.find_all())}개")

    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("🔍 카페 검색 상세 디버거")
    print("="*60)

    query = input("\n검색어 입력 (Enter=육아): ").strip() or "육아"
    debug_cafe_detail(query)

    print("\n" + "="*60)
    print("✅ 디버깅 완료!")
    print("="*60)

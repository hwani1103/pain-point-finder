#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카페 게시글 본문 추출 디버그
실제 게시글을 방문해서 HTML 구조 분석
"""

import requests
from bs4 import BeautifulSoup

# 테스트할 URL (위 결과에서 가져옴)
test_url = "https://cafe.naver.com/remonterrace/34281342"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("="*60)
print("카페 게시글 본문 추출 디버그")
print("="*60)
print(f"\n테스트 URL: {test_url}")

try:
    # 1단계: 메인 페이지 접근
    print("\n[1단계] 메인 페이지 접근...")
    response = requests.get(test_url, headers=headers, timeout=10)
    print(f"응답 코드: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # iframe 확인
    print("\n[2단계] iframe 확인...")
    iframe = soup.find('iframe', {'id': 'cafe_main'})

    if iframe:
        iframe_src = iframe.get('src', '')
        print(f"✓ iframe 발견!")
        print(f"  src: {iframe_src[:100]}...")

        if iframe_src and iframe_src not in ['about:blank', 'about:', '#']:
            if not iframe_src.startswith('http'):
                iframe_src = 'https://cafe.naver.com' + iframe_src

            print(f"\n[3단계] iframe 내부 페이지 접근...")
            print(f"  URL: {iframe_src[:100]}...")

            response = requests.get(iframe_src, headers=headers, timeout=10)
            print(f"  응답 코드: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"  ✗ 무효한 iframe src: {iframe_src}")
    else:
        print("✗ iframe을 찾지 못함 (iframe 없는 구조일 수도 있음)")

    # HTML 파일로 저장
    print("\n[4단계] HTML 저장...")
    with open('debug_cafe_post.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("✓ debug_cafe_post.html 저장 완료")

    # 여러 셀렉터 시도
    print("\n[5단계] 본문 셀렉터 테스트...")
    print("="*60)

    selectors = [
        ('div.se-main-container', '스마트에디터'),
        ('div#postViewArea', '구버전 에디터'),
        ('div.article_viewer', '게시글 뷰어'),
        ('div.ArticleContentBox', '게시글 컨텐츠'),
        ('div#app', 'Vue 앱'),
        ('div[class*="article"]', 'article 클래스'),
        ('div[class*="content"]', 'content 클래스'),
        ('div[class*="post"]', 'post 클래스'),
    ]

    for selector, desc in selectors:
        elem = soup.select_one(selector)
        if elem:
            text = elem.get_text(strip=True)
            print(f"\n✓ {selector} ({desc})")
            print(f"  발견됨! 텍스트 길이: {len(text)}자")
            print(f"  내용 미리보기: {text[:100]}...")
        else:
            print(f"\n✗ {selector} ({desc})")
            print(f"  없음")

    # 전체 텍스트 확인
    print("\n" + "="*60)
    print("전체 페이지 텍스트 (처음 500자):")
    print("="*60)
    full_text = soup.get_text(strip=True)
    print(full_text[:500])
    print(f"\n총 텍스트 길이: {len(full_text)}자")

except Exception as e:
    print(f"\n오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("디버그 완료!")
print("debug_cafe_post.html 파일을 확인하세요.")
print("="*60)

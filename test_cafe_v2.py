#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cafe Crawler V2 빠른 테스트
"""

from cafe_crawler_v2 import CafePainPointCrawlerV2

print("="*60)
print("🧪 Cafe Crawler V2 테스트")
print("="*60)

# 크롤러 생성 (페이지당 3개만 방문)
crawler = CafePainPointCrawlerV2(max_posts_per_page=3)

# 테스트 검색
print("\n테스트 검색어: '육아'")
print("검색 페이지: 1페이지")
print("방문할 게시글: 3개")
print("\n시작합니다...\n")

crawler.search_cafe_posts('육아', max_pages=1)

# 결과 출력
print("\n" + "="*60)
print("테스트 결과:")
print("="*60)

if crawler.results:
    print(f"\n✅ {len(crawler.results)}개의 Pain Point 발견!")

    for idx, result in enumerate(crawler.results[:3], 1):
        print(f"\n[{idx}]")
        print(f"  제목: {result['제목'][:50]}...")
        print(f"  카페: {result['카페명']}")
        print(f"  본문: {result['본문'][:100]}...")
        print(f"  본문 길이: {result['본문_전체_길이']}자")
        print(f"  키워드: {result['매칭_키워드']}")
else:
    print("\n❌ Pain Point를 발견하지 못했습니다.")
    print("검색어나 설정을 조정해보세요.")

print("\n" + "="*60)
print("테스트 완료!")
print("="*60)

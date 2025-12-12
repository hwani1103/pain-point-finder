#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pain Point Finder - 대화형 버전
직접 검색어와 키워드를 입력할 수 있습니다
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re
from collections import Counter
from urllib.parse import quote


class PainPointCrawler:
    """네이버 블로그에서 Pain Point를 찾는 크롤러"""

    # 기본 Pain Point 키워드 리스트
    DEFAULT_KEYWORDS = [
        '불편해', '불편하다', '불편한',
        '어려워', '어렵다', '어려운',
        '없나요', '없을까', '없네',
        '왜 이런 게 없지', '왜 없',
        '개선됐으면', '개선되면', '개선이 필요',
        '힘들어', '힘들다', '힘든',
        '짜증', '화나',
        '답답해', '답답하다', '답답한',
        '불만', '문제가', '문제점',
        '고치면', '고쳐', '바꿔',
        '왜 이래', '왜 이렇게',
        '불편', '개선', '해결'
    ]

    def __init__(self, custom_keywords=None):
        """
        크롤러 초기화

        Args:
            custom_keywords: 사용자 정의 키워드 리스트 (None이면 기본 키워드 사용)
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []

        # 키워드 설정
        if custom_keywords:
            self.keywords = custom_keywords
        else:
            self.keywords = self.DEFAULT_KEYWORDS

    def search_naver_blog(self, query, max_pages=3):
        """
        네이버 블로그 검색

        Args:
            query: 검색할 키워드
            max_pages: 검색할 페이지 수
        """
        print(f"\n=== 네이버 블로그 검색 시작: '{query}' ===")
        print(f"검색 페이지 수: {max_pages}")

        for page in range(1, max_pages + 1):
            start = (page - 1) * 10 + 1
            url = f"https://search.naver.com/search.naver?where=blog&query={quote(query)}&start={start}"

            print(f"\n[페이지 {page}/{max_pages}] 크롤링 중...")

            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # 네이버 블로그 검색 결과 파싱
                blog_items = soup.select('div.view_wrap')

                if not blog_items:
                    blog_items = soup.select('li.bx')

                print(f"  발견된 블로그 포스트: {len(blog_items)}개")

                for idx, item in enumerate(blog_items, 1):
                    try:
                        # 제목과 링크
                        title_elem = item.select_one('a.title_link') or item.select_one('a.api_txt_lines')
                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')

                        # 본문 내용
                        content_elem = item.select_one('div.dsc_link') or item.select_one('dd.sh_blog_passage')
                        content = content_elem.get_text(strip=True) if content_elem else ''

                        # 날짜
                        date_elem = item.select_one('span.sub_time') or item.select_one('dd.txt_inline')
                        date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y.%m.%d')

                        # 전체 텍스트 (제목 + 본문)
                        full_text = f"{title} {content}"

                        # Pain Point 키워드 매칭
                        matched_keywords = self._find_pain_keywords(full_text)

                        if matched_keywords:
                            print(f"    ✓ [{idx}] Pain Point 발견: {title[:30]}... (키워드: {', '.join(matched_keywords)})")

                            self.results.append({
                                '날짜': date_str,
                                '제목': title,
                                '본문_일부': content[:200] if content else '',
                                '링크': link,
                                '매칭_키워드': ', '.join(matched_keywords),
                                '키워드_개수': len(matched_keywords),
                                '검색어': query
                            })

                    except Exception as e:
                        print(f"    ✗ 항목 처리 오류: {e}")
                        continue

                # 요청 간 딜레이 (네이버 서버 부하 방지)
                time.sleep(1)

            except Exception as e:
                print(f"  ✗ 페이지 {page} 크롤링 오류: {e}")
                continue

        print(f"\n'{query}' 검색 완료: {len([r for r in self.results if r['검색어'] == query])}개 발견")

    def _find_pain_keywords(self, text):
        """텍스트에서 Pain Point 키워드 찾기"""
        matched = []
        text_lower = text.lower()

        for keyword in self.keywords:
            if keyword in text_lower or keyword in text:
                matched.append(keyword)

        return list(set(matched))  # 중복 제거

    def save_to_csv(self, filename=None):
        """결과를 CSV 파일로 저장"""
        if not self.results:
            print("\n저장할 데이터가 없습니다.")
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'pain_points_{timestamp}.csv'

        print(f"\n=== CSV 파일 저장 중 ===")

        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(self.results)}개 항목")

        # 통계 파일도 저장
        stats_filename = filename.replace('.csv', '_통계.csv')
        self._save_statistics_csv(stats_filename, df)

        return filename

    def _save_statistics_csv(self, filename, df):
        """통계를 CSV 파일로 저장"""
        all_keywords = []
        for keywords_str in df['매칭_키워드']:
            keywords = [k.strip() for k in keywords_str.split(',')]
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        stats_df = pd.DataFrame([
            {'키워드': keyword, '빈도수': count}
            for keyword, count in keyword_counts.most_common()
        ])

        query_stats = df.groupby('검색어').size().reset_index(name='발견_개수')

        stats_df.to_csv(filename, index=False, encoding='utf-8-sig')

        query_filename = filename.replace('통계.csv', '검색어_통계.csv')
        query_stats.to_csv(query_filename, index=False, encoding='utf-8-sig')

        print(f"✓ 통계 저장 완료: {filename}, {query_filename}")

    def show_statistics(self):
        """통계 출력"""
        if not self.results:
            print("\n통계를 생성할 데이터가 없습니다.")
            return

        print("\n" + "="*60)
        print("📊 Pain Point 통계")
        print("="*60)

        print(f"\n총 발견 개수: {len(self.results)}개")

        all_keywords = []
        for result in self.results:
            keywords = result['매칭_키워드'].split(', ')
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        print(f"\n🔑 상위 10개 키워드:")
        for keyword, count in keyword_counts.most_common(10):
            print(f"  {keyword}: {count}회")

        query_counts = Counter([r['검색어'] for r in self.results])
        print(f"\n🔍 검색어별 발견 개수:")
        for query, count in query_counts.items():
            print(f"  {query}: {count}개")


def main():
    """대화형 메인 실행 함수"""
    print("="*60)
    print("🔍 Pain Point Finder - 대화형 버전")
    print("="*60)

    # 1. 키워드 설정
    print("\n[1단계] Pain Point 키워드 설정")
    print("-" * 60)
    print("기본 키워드를 사용하시겠습니까?")
    print("(불편해, 어려워, 없나요, 개선됐으면 등 20개)")

    use_default = input("\n기본 키워드 사용? (y/n, Enter=y): ").strip().lower()

    custom_keywords = None
    if use_default != '' and use_default != 'y':
        print("\n사용할 키워드를 쉼표(,)로 구분하여 입력하세요:")
        print("예: 불편해,어려워,힘들어,짜증나")
        keyword_input = input("키워드 입력: ").strip()

        if keyword_input:
            custom_keywords = [k.strip() for k in keyword_input.split(',')]
            print(f"\n✓ {len(custom_keywords)}개 키워드 설정 완료: {', '.join(custom_keywords)}")

    # 크롤러 생성
    crawler = PainPointCrawler(custom_keywords=custom_keywords)

    # 2. 검색어 입력
    print("\n[2단계] 검색어 입력")
    print("-" * 60)
    print("네이버 블로그에서 검색할 키워드를 입력하세요.")
    print("여러 개 검색하려면 쉼표(,)로 구분하세요.")
    print("예: 일상 불편함,생활 불편,앱 사용 어려움")

    search_input = input("\n검색어 입력: ").strip()

    if not search_input:
        print("\n검색어가 입력되지 않았습니다. 기본 검색어를 사용합니다.")
        search_queries = ['일상 불편함', '생활 불편']
    else:
        search_queries = [q.strip() for q in search_input.split(',')]

    print(f"\n✓ {len(search_queries)}개 검색어 설정 완료")

    # 3. 페이지 수 입력
    print("\n[3단계] 검색 페이지 수 설정")
    print("-" * 60)
    print("각 검색어당 몇 페이지씩 검색할까요?")
    print("(1페이지 = 약 10개 블로그 포스트)")

    pages_input = input("페이지 수 (Enter=2): ").strip()

    try:
        max_pages = int(pages_input) if pages_input else 2
        if max_pages < 1:
            max_pages = 2
    except:
        max_pages = 2

    print(f"\n✓ 페이지 수: {max_pages}")

    # 4. 크롤링 시작
    print("\n" + "="*60)
    print("🚀 크롤링 시작!")
    print("="*60)

    for query in search_queries:
        crawler.search_naver_blog(query, max_pages=max_pages)

    # 5. 결과 확인
    if not crawler.results:
        print("\n❌ Pain Point를 발견하지 못했습니다.")
        print("다른 검색어나 키워드를 시도해보세요.")
        return

    print(f"\n✅ 총 {len(crawler.results)}개의 Pain Point를 발견했습니다!")

    # 6. 통계 출력
    crawler.show_statistics()

    # 7. 파일 저장
    print("\n[최종단계] 파일 저장")
    print("-" * 60)
    save = input("결과를 파일로 저장하시겠습니까? (y/n, Enter=y): ").strip().lower()

    if save == '' or save == 'y':
        csv_filename = crawler.save_to_csv()

        print("\n" + "="*60)
        print(f"✅ 저장 완료!")
        print(f"📁 생성된 파일:")
        print(f"  - {csv_filename}")
        print(f"  - {csv_filename.replace('.csv', '_통계.csv')}")
        print(f"  - {csv_filename.replace('.csv', '_검색어_통계.csv')}")
        print("="*60)
    else:
        print("\n파일 저장을 건너뛰었습니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n\n오류 발생: {e}")
        print("프로그램을 다시 실행해주세요.")

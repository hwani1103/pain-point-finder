#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pain Point Finder - 네이버 블로그 크롤러
사람들의 불편함/문제점을 발굴하는 크롤러
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

    # Pain Point 키워드 리스트
    PAIN_POINT_KEYWORDS = [
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

    def __init__(self):
        """크롤러 초기화"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []

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
                # 네이버 블로그 검색 결과 파싱 (2024년 업데이트된 구조)
                blog_items = soup.select('div.api_subject_bx')

                if not blog_items:
                    # 이전 구조 시도
                    blog_items = soup.select('div.view_wrap')

                if not blog_items:
                    blog_items = soup.select('li.bx')

                print(f"  발견된 블로그 포스트: {len(blog_items)}개")

                for idx, item in enumerate(blog_items, 1):
                    try:
                        # 제목과 링크 추출 (여러 가지 셀렉터 시도)
                        title_elem = (item.select_one('a.api_txt_lines') or
                                    item.select_one('a.title_link') or
                                    item.select_one('a.sub_txt') or
                                    item.select_one('a[href*="blog.naver"]'))

                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')

                        # 본문 추출 (여러 가지 셀렉터 시도)
                        content_elem = (item.select_one('dd.api_txt_lines') or
                                      item.select_one('div.dsc_link') or
                                      item.select_one('dd.sh_blog_passage') or
                                      item.select_one('div.api_txt'))
                        content = content_elem.get_text(strip=True) if content_elem else ''

                        # 날짜 추출 (여러 가지 셀렉터 시도)
                        date_elem = (item.select_one('span.sub_time') or
                                   item.select_one('dd.txt_inline') or
                                   item.select_one('span.sub_txt'))
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

        print(f"\n총 {len(self.results)}개의 Pain Point 발견!")

    def _find_pain_keywords(self, text):
        """텍스트에서 Pain Point 키워드 찾기"""
        matched = []
        text_lower = text.lower()

        for keyword in self.PAIN_POINT_KEYWORDS:
            if keyword in text_lower or keyword in text:
                matched.append(keyword)

        return list(set(matched))  # 중복 제거

    def save_to_csv(self, filename=None):
        """
        결과를 CSV 파일로 저장

        Args:
            filename: 저장할 파일명 (None이면 자동 생성)
        """
        if not self.results:
            print("\n저장할 데이터가 없습니다.")
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'pain_points_{timestamp}.csv'

        print(f"\n=== CSV 파일 저장 중 ===")

        # 데이터프레임 생성
        df = pd.DataFrame(self.results)

        # CSV 저장 (UTF-8 with BOM for Excel compatibility)
        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(self.results)}개 항목")

        # 통계 파일도 저장
        stats_filename = filename.replace('.csv', '_통계.csv')
        self._save_statistics_csv(stats_filename, df)

        return filename

    def _save_statistics_csv(self, filename, df):
        """통계를 CSV 파일로 저장"""
        # 키워드별 빈도수 계산
        all_keywords = []
        for keywords_str in df['매칭_키워드']:
            keywords = [k.strip() for k in keywords_str.split(',')]
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        # 통계 데이터프레임 생성
        stats_df = pd.DataFrame([
            {'키워드': keyword, '빈도수': count}
            for keyword, count in keyword_counts.most_common()
        ])

        # 검색어별 통계
        query_stats = df.groupby('검색어').size().reset_index(name='발견_개수')

        # CSV로 저장
        stats_df.to_csv(filename, index=False, encoding='utf-8-sig')

        query_filename = filename.replace('통계.csv', '검색어_통계.csv')
        query_stats.to_csv(query_filename, index=False, encoding='utf-8-sig')

        print(f"✓ 통계 저장 완료: {filename}")

    def save_to_excel(self, filename=None):
        """
        결과를 엑셀 파일로 저장

        Args:
            filename: 저장할 파일명 (None이면 자동 생성)
        """
        if not self.results:
            print("\n저장할 데이터가 없습니다.")
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'pain_points_{timestamp}.xlsx'

        print(f"\n=== 엑셀 파일 저장 중 ===")

        # 데이터프레임 생성
        df = pd.DataFrame(self.results)

        # 엑셀 writer 생성
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 메인 데이터 시트
            df.to_excel(writer, sheet_name='Pain Points', index=False)

            # 통계 시트
            self._create_statistics_sheet(writer, df)

        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(self.results)}개 항목")

        return filename

    def _create_statistics_sheet(self, writer, df):
        """통계 시트 생성"""
        # 키워드별 빈도수 계산
        all_keywords = []
        for keywords_str in df['매칭_키워드']:
            keywords = [k.strip() for k in keywords_str.split(',')]
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        # 통계 데이터프레임 생성
        stats_df = pd.DataFrame([
            {'키워드': keyword, '빈도수': count}
            for keyword, count in keyword_counts.most_common()
        ])

        # 검색어별 통계
        query_stats = df.groupby('검색어').size().reset_index(name='발견_개수')

        # 통계 시트에 저장
        stats_df.to_excel(writer, sheet_name='키워드_통계', index=False)
        query_stats.to_excel(writer, sheet_name='검색어_통계', index=False, startrow=0)

    def show_statistics(self):
        """통계 출력"""
        if not self.results:
            print("\n통계를 생성할 데이터가 없습니다.")
            return

        print("\n" + "="*60)
        print("📊 Pain Point 통계")
        print("="*60)

        # 전체 통계
        print(f"\n총 발견 개수: {len(self.results)}개")

        # 키워드별 빈도수
        all_keywords = []
        for result in self.results:
            keywords = result['매칭_키워드'].split(', ')
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        print(f"\n🔑 상위 10개 키워드:")
        for keyword, count in keyword_counts.most_common(10):
            print(f"  {keyword}: {count}회")

        # 검색어별 통계
        query_counts = Counter([r['검색어'] for r in self.results])
        print(f"\n🔍 검색어별 발견 개수:")
        for query, count in query_counts.items():
            print(f"  {query}: {count}개")


def main():
    """메인 실행 함수"""
    print("="*60)
    print("🔍 Pain Point Finder - 네이버 블로그 크롤러")
    print("="*60)

    # 크롤러 생성
    crawler = PainPointCrawler()

    # 검색할 키워드들 (예시)
    search_queries = [
        '일상 불편함',
        '생활 불편',
        '앱 사용 불편'
    ]

    print("\n📝 검색 키워드:")
    for query in search_queries:
        print(f"  - {query}")

    # 각 키워드로 검색
    for query in search_queries:
        crawler.search_naver_blog(query, max_pages=2)

    # 통계 출력
    crawler.show_statistics()

    # 파일 저장 (CSV와 Excel 모두)
    print("\n" + "="*60)
    print("💾 결과 저장 중...")
    print("="*60)

    csv_filename = crawler.save_to_csv()
    excel_filename = crawler.save_to_excel()

    print("\n" + "="*60)
    print(f"✅ 크롤링 완료!")
    print(f"📁 결과 파일:")
    print(f"  - CSV: {csv_filename}")
    print(f"  - Excel: {excel_filename}")
    print("\n💡 팁: 엑셀이 없다면 CSV 파일을 Google Sheets나 메모장으로 열 수 있습니다!")
    print("="*60)


if __name__ == "__main__":
    main()

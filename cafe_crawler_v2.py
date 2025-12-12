#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pain Point Finder - 네이버 카페 크롤러 V2 (실제 게시글 방문)
검색 결과에서 링크를 수집한 뒤, 각 게시글을 방문하여 전체 내용을 추출합니다.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
from collections import Counter
from urllib.parse import quote
import re


class CafePainPointCrawlerV2:
    """네이버 카페 게시글을 실제 방문하여 Pain Point를 찾는 크롤러"""

    # Pain Point 키워드 (기존 + 감정 표현)
    PAIN_POINT_KEYWORDS = [
        # 기존 키워드
        '불편해', '불편하다', '불편한', '불편',
        '어려워', '어렵다', '어려운',
        '없나요', '없을까', '없네', '왜 없',
        '개선됐으면', '개선되면', '개선이 필요', '개선',
        '힘들어', '힘들다', '힘든',
        '짜증', '화나',
        '답답해', '답답하다', '답답한',
        '불만', '문제가', '문제점',
        '고치면', '고쳐', '바꿔',
        '왜 이래', '왜 이렇게',
        '해결',

        # 날것의 감정 표현 (카페/커뮤니티용)
        'ㅠㅠ', 'ㅜㅜ', 'ㅡㅡ',
        '진짜', '정말', '너무',
        '아', '에휴', '하',
        '개', 'ㅈㄴ',
        '미치', '죽',
        '짜증나', '빡쳐',
        '열받', '빡치',
        '최악', '망함',
        '실망', '헐',
    ]

    def __init__(self, max_posts_per_page=5):
        """
        크롤러 초기화

        Args:
            max_posts_per_page: 각 검색 페이지에서 방문할 최대 게시글 수 (기본 5개)
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []
        self.max_posts_per_page = max_posts_per_page

    def search_cafe_posts(self, query, max_pages=3):
        """
        네이버 카페 게시글 검색 및 실제 내용 추출 (2-Stage)

        Stage 1: 검색 결과에서 카페 게시글 링크 수집
        Stage 2: 각 링크를 방문하여 전체 내용 추출

        Args:
            query: 검색할 키워드
            max_pages: 검색할 페이지 수
        """
        print(f"\n=== 네이버 카페 게시글 검색 시작: '{query}' ===")
        print(f"검색 페이지 수: {max_pages}")
        print(f"페이지당 방문할 게시글 수: {self.max_posts_per_page}개")

        for page in range(1, max_pages + 1):
            start = (page - 1) * 10 + 1

            # Stage 1: 검색 결과에서 링크 수집
            url = f"https://search.naver.com/search.naver?where=article&query={quote(query)}&start={start}"

            print(f"\n[페이지 {page}/{max_pages}] 링크 수집 중...")

            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # 카페 게시글 링크 찾기
                cafe_links = []

                # 모든 링크 요소 찾기
                all_links = soup.find_all('a', href=True)

                for link_elem in all_links:
                    href = link_elem.get('href', '')
                    title = link_elem.get_text(strip=True)

                    # 카페 게시글 링크만 필터링 (더 관대한 조건)
                    if 'cafe.naver.com' in href:
                        # 무효한 URL 제외
                        if 'about:blank' in href or href.startswith('#') or not href.startswith('http'):
                            continue

                        # 제외할 패턴들
                        skip_patterns = [
                            '/cafehome',  # 카페 홈
                            '/MyCafeIntro',  # 카페 소개
                            '/CafeList',  # 카페 목록
                            '/ArticleList.nhn',  # 게시판 목록
                            'naver.com/ca-fe',  # 메인
                        ]

                        # 제외 패턴이 있으면 스킵
                        if any(pattern in href for pattern in skip_patterns):
                            continue

                        # 광고나 메타정보 제외
                        if title and len(title) > 5 and '광고' not in title and '이유' not in title:
                            cafe_links.append({
                                'title': title,
                                'url': href
                            })

                # 중복 제거 (URL 기준)
                seen_urls = set()
                unique_links = []
                for link in cafe_links:
                    if link['url'] not in seen_urls:
                        seen_urls.add(link['url'])
                        unique_links.append(link)

                print(f"  발견된 카페 게시글 링크: {len(unique_links)}개")

                # 디버그: 처음 3개 링크 출력
                if unique_links:
                    print(f"\n  📋 링크 샘플 (처음 3개):")
                    for i, link in enumerate(unique_links[:3], 1):
                        print(f"    {i}. {link['title'][:40]}...")
                else:
                    print(f"\n  ⚠️  카페 링크를 찾지 못했습니다!")
                    print(f"     전체 링크 개수: {len(all_links)}개")
                    print(f"     cafe.naver.com 포함 링크: {len([l for l in all_links if 'cafe.naver.com' in l.get('href', '')])}개")

                # Stage 2: 각 게시글 방문하여 전체 내용 추출
                posts_visited = 0
                for idx, link_info in enumerate(unique_links[:self.max_posts_per_page], 1):
                    if posts_visited >= self.max_posts_per_page:
                        break

                    print(f"\n  [{idx}/{min(len(unique_links), self.max_posts_per_page)}] 게시글 방문 중...")
                    print(f"      제목: {link_info['title'][:40]}...")

                    # 실제 게시글 내용 추출
                    post_data = self._extract_post_content(link_info['url'], link_info['title'], query)

                    if post_data:
                        posts_visited += 1

                        # Pain Point 키워드 매칭
                        full_text = f"{post_data['제목']} {post_data['본문']}"
                        matched_keywords = self._find_pain_keywords(full_text)

                        if matched_keywords:
                            print(f"      ✓ Pain Point 발견! 키워드: {', '.join(matched_keywords[:5])}")

                            post_data['매칭_키워드'] = ', '.join(matched_keywords)
                            post_data['키워드_개수'] = len(matched_keywords)
                            post_data['검색어'] = query

                            self.results.append(post_data)
                        else:
                            print(f"      ✗ Pain Point 키워드 없음")

                    # 서버 부하 방지
                    time.sleep(2)

                # 페이지 간 딜레이
                time.sleep(1.5)

            except Exception as e:
                print(f"  ✗ 페이지 {page} 처리 오류: {e}")
                continue

        print(f"\n'{query}' 검색 완료: {len([r for r in self.results if r['검색어'] == query])}개 Pain Point 발견")

    def _extract_post_content(self, url, title, query):
        """
        실제 카페 게시글 페이지를 방문하여 전체 내용 추출

        Args:
            url: 게시글 URL
            title: 게시글 제목
            query: 검색어

        Returns:
            dict: 게시글 정보 (제목, 본문, 날짜, 카페명, 링크)
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # iframe 내부의 실제 게시글 URL 찾기
            # 네이버 카페는 보통 iframe으로 게시글을 감싸고 있음
            iframe = soup.find('iframe', {'id': 'cafe_main'})

            if iframe and iframe.get('src'):
                iframe_url = iframe['src']
                if not iframe_url.startswith('http'):
                    iframe_url = 'https://cafe.naver.com' + iframe_url

                # iframe 내부 페이지 요청
                response = requests.get(iframe_url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

            # 게시글 본문 추출 (여러 셀렉터 시도)
            content = ''

            # 시도 1: div.se-main-container (스마트에디터)
            content_elem = soup.select_one('div.se-main-container')
            if content_elem:
                content = content_elem.get_text(strip=True)

            # 시도 2: div#postViewArea
            if not content:
                content_elem = soup.select_one('div#postViewArea')
                if content_elem:
                    content = content_elem.get_text(strip=True)

            # 시도 3: div.article_viewer
            if not content:
                content_elem = soup.select_one('div.article_viewer')
                if content_elem:
                    content = content_elem.get_text(strip=True)

            # 시도 4: div.ArticleContentBox
            if not content:
                content_elem = soup.select_one('div.ArticleContentBox')
                if content_elem:
                    content = content_elem.get_text(strip=True)

            # 본문이 너무 짧으면 무시
            if not content or len(content) < 20:
                print(f"      ✗ 본문 추출 실패 (너무 짧음: {len(content)}자)")
                return None

            # 카페명 추출
            cafe_name = self._extract_cafe_name_from_page(soup, url)

            # 날짜 추출
            date_str = self._extract_date_from_page(soup)

            return {
                '날짜': date_str,
                '카페명': cafe_name,
                '제목': title,
                '본문': content[:500],  # 처음 500자만 저장
                '본문_전체_길이': len(content),
                '링크': url,
            }

        except Exception as e:
            print(f"      ✗ 게시글 추출 오류: {e}")
            return None

    def _extract_cafe_name_from_page(self, soup, url):
        """카페명 추출"""
        try:
            # 시도 1: h1.d-none 또는 a.cafe-name
            cafe_elem = soup.select_one('a.gm-tcol-c') or soup.select_one('h1.d-none')
            if cafe_elem:
                return cafe_elem.get_text(strip=True)

            # 시도 2: URL에서 카페 ID 추출
            match = re.search(r'clubid=(\d+)', url)
            if match:
                return f"카페ID_{match.group(1)}"

            return '알 수 없음'
        except:
            return '알 수 없음'

    def _extract_date_from_page(self, soup):
        """날짜 추출"""
        try:
            # 시도 1: span.date
            date_elem = soup.select_one('span.date') or soup.select_one('td.date')
            if date_elem:
                return date_elem.get_text(strip=True)

            # 시도 2: div.article_info에서 날짜 찾기
            info_elem = soup.select_one('div.article_info')
            if info_elem:
                text = info_elem.get_text()
                # "2024.12.12" 형식 찾기
                match = re.search(r'\d{4}\.\d{1,2}\.\d{1,2}', text)
                if match:
                    return match.group(0)

            return datetime.now().strftime('%Y.%m.%d')
        except:
            return datetime.now().strftime('%Y.%m.%d')

    def _find_pain_keywords(self, text):
        """텍스트에서 Pain Point 키워드 찾기"""
        matched = []
        text_lower = text.lower()

        for keyword in self.PAIN_POINT_KEYWORDS:
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
            filename = f'cafe_pain_points_v2_{timestamp}.csv'

        print(f"\n=== CSV 파일 저장 중 ===")

        # 메인 CSV 저장
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['날짜', '카페명', '제목', '본문', '본문_전체_길이', '링크', '매칭_키워드', '키워드_개수', '검색어']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.results:
                writer.writerow(row)

        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(self.results)}개 항목")

        # 통계 파일 저장
        stats_filename = filename.replace('.csv', '_통계.csv')
        self._save_statistics_csv(stats_filename)

        return filename

    def _save_statistics_csv(self, filename):
        """통계를 CSV 파일로 저장"""
        # 키워드별 빈도수 계산
        all_keywords = []
        for result in self.results:
            keywords = [k.strip() for k in result['매칭_키워드'].split(',')]
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        # 키워드 통계 저장
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['키워드', '빈도수'])
            for keyword, count in keyword_counts.most_common():
                writer.writerow([keyword, count])

        # 카페별 통계 저장
        cafe_filename = filename.replace('통계.csv', '카페별_통계.csv')
        cafe_counts = Counter([r['카페명'] for r in self.results])

        with open(cafe_filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['카페명', '발견_개수'])
            for cafe, count in cafe_counts.most_common():
                writer.writerow([cafe, count])

        print(f"✓ 통계 저장 완료: {filename}, {cafe_filename}")

    def show_statistics(self):
        """통계 출력"""
        if not self.results:
            print("\n통계를 생성할 데이터가 없습니다.")
            return

        print("\n" + "="*60)
        print("📊 카페 Pain Point 통계 (V2 - 전체 게시글 기반)")
        print("="*60)

        print(f"\n총 발견 개수: {len(self.results)}개")

        # 키워드 통계
        all_keywords = []
        for result in self.results:
            keywords = result['매칭_키워드'].split(', ')
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        print(f"\n🔑 상위 10개 키워드:")
        for keyword, count in keyword_counts.most_common(10):
            print(f"  {keyword}: {count}회")

        # 카페별 통계
        cafe_counts = Counter([r['카페명'] for r in self.results])
        print(f"\n☕ 상위 카페:")
        for cafe, count in cafe_counts.most_common(5):
            print(f"  {cafe}: {count}개")

        # 검색어별 통계
        query_counts = Counter([r['검색어'] for r in self.results])
        print(f"\n🔍 검색어별 발견 개수:")
        for query, count in query_counts.items():
            print(f"  {query}: {count}개")

        # 본문 길이 통계
        total_length = sum([r['본문_전체_길이'] for r in self.results])
        avg_length = total_length / len(self.results) if self.results else 0
        print(f"\n📝 본문 길이:")
        print(f"  평균: {avg_length:.0f}자")
        print(f"  총합: {total_length:,}자")


def main():
    """대화형 메인 실행 함수"""
    print("="*60)
    print("🔍 Pain Point Finder - 네이버 카페 크롤러 V2")
    print("="*60)
    print("\n✅ 실제 게시글을 방문하여 전체 내용을 분석합니다!")
    print("✅ 검색 결과 미리보기가 아닌 진짜 게시글 본문을 크롤링합니다!")

    # 크롤러 생성
    print("\n[0단계] 크롤러 설정")
    print("-" * 60)
    posts_per_page = input("각 검색 페이지에서 방문할 게시글 수 (Enter=5): ").strip()

    try:
        posts_per_page = int(posts_per_page) if posts_per_page else 5
        if posts_per_page < 1:
            posts_per_page = 5
    except:
        posts_per_page = 5

    crawler = CafePainPointCrawlerV2(max_posts_per_page=posts_per_page)

    # 검색어 입력
    print("\n[1단계] 검색어 입력")
    print("-" * 60)
    print("카페에서 검색할 키워드를 입력하세요.")
    print("여러 개 검색하려면 쉼표(,)로 구분하세요.")
    print("\n추천 검색어:")
    print("  - 육아: 육아 힘들어, 아이 키우기 불편")
    print("  - 직장: 회사 불편, 직장 짜증")
    print("  - 생활: 주방 불편, 청소 어려워")

    search_input = input("\n검색어 입력 (Enter=기본값): ").strip()

    if not search_input:
        search_queries = ['육아 힘들어', '직장 불편']
        print(f"기본 검색어 사용: {', '.join(search_queries)}")
    else:
        search_queries = [q.strip() for q in search_input.split(',')]

    # 페이지 수 입력
    print("\n[2단계] 검색 페이지 수 설정")
    print("-" * 60)
    pages_input = input("페이지 수 (Enter=2): ").strip()

    try:
        max_pages = int(pages_input) if pages_input else 2
        if max_pages < 1:
            max_pages = 2
    except:
        max_pages = 2

    # 크롤링 시작
    print("\n" + "="*60)
    print("🚀 카페 크롤링 시작!")
    print(f"⚠️  실제 게시글을 방문하므로 시간이 걸립니다...")
    print(f"   (페이지당 약 {posts_per_page * 2}초 + 게시글당 2초)")
    print("="*60)

    for query in search_queries:
        crawler.search_cafe_posts(query, max_pages=max_pages)

    # 결과 확인
    if not crawler.results:
        print("\n❌ Pain Point를 발견하지 못했습니다.")
        print("다른 검색어를 시도해보세요.")
        return

    print(f"\n✅ 총 {len(crawler.results)}개의 Pain Point를 발견했습니다!")

    # 통계 출력
    crawler.show_statistics()

    # 파일 저장
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
        print(f"  - {csv_filename.replace('.csv', '_카페별_통계.csv')}")
        print("\n💡 CSV 파일을 Google Sheets나 메모장으로 열 수 있습니다!")
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

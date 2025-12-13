#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pain Point Finder - 디시인사이드 크롤러
실제 게시글을 방문하여 전체 내용을 추출합니다.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
from collections import Counter

class DCInsidePainPointCrawler:
    """디시인사이드 갤러리 크롤러"""

    # Pain Point 키워드
    PAIN_POINT_KEYWORDS = [
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

    def __init__(self, custom_keywords=None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []

        # 키워드 설정 (커스텀 키워드가 있으면 사용, 없으면 기본)
        if custom_keywords:
            self.keywords = custom_keywords
            print(f"\n✓ 사용자 지정 키워드 {len(custom_keywords)}개 적용")
        else:
            self.keywords = self.PAIN_POINT_KEYWORDS
            print(f"\n✓ 기본 키워드 {len(self.keywords)}개 사용")

    def search_gallery(self, gallery_id, max_pages=3, target_pain_points=5):
        """
        디시인사이드 갤러리 크롤링

        Args:
            gallery_id: 갤러리 ID (예: 'baseball_new11', 'stock')
            max_pages: 크롤링할 페이지 수
            target_pain_points: 목표 Pain Point 개수 (이 개수만큼 찾을 때까지 계속 탐색)
        """
        print(f"\n=== 디시인사이드 갤러리 크롤링 시작: '{gallery_id}' ===")
        print(f"페이지 수: {max_pages}")
        print(f"목표 Pain Point: {target_pain_points}개 (키워드 있는 게시글만)")

        for page in range(1, max_pages + 1):
            url = f"https://gall.dcinside.com/board/lists/?id={gallery_id}&page={page}"

            print(f"\n[페이지 {page}/{max_pages}] 크롤링 중...")

            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # 게시글 목록 찾기
                posts = soup.select('tr.ub-content')
                print(f"  발견된 게시글: {len(posts)}개")

                # 각 게시글 처리 (키워드 있는 것을 찾을 때까지)
                page_pain_points = 0  # 이 페이지에서 찾은 Pain Point 개수
                for idx, post in enumerate(posts, 1):
                    # 이미 목표 달성했으면 중단
                    current_total = len([r for r in self.results if r.get('갤러리') == gallery_id])
                    if current_total >= target_pain_points:
                        print(f"\n  ✓ 목표 달성! ({current_total}개 Pain Point 발견)")
                        break

                    try:
                        # 제목과 링크 추출
                        title_elem = post.select_one('td.gall_tit a')
                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)
                        href = title_elem.get('href', '')

                        # 공지, 설문 등 제외
                        if not href or 'view' not in href:
                            continue

                        # 절대 URL 생성
                        if href.startswith('/'):
                            post_url = f"https://gall.dcinside.com{href}"
                        else:
                            post_url = href

                        current_count = len([r for r in self.results if r.get('갤러리') == gallery_id])
                        print(f"\n  [{idx}] 게시글 방문 중... (현재 {current_count}/{target_pain_points})")
                        print(f"      제목: {title[:40]}...")

                        # 게시글 내용 추출
                        post_data = self._extract_post_content(post_url, title, gallery_id)

                        if post_data:
                            # Pain Point 키워드 매칭
                            full_text = f"{post_data['제목']} {post_data['본문']}"
                            matched_keywords = self._find_pain_keywords(full_text)

                            if matched_keywords:
                                print(f"      ✓ Pain Point 발견! 키워드: {', '.join(matched_keywords[:5])}")

                                post_data['매칭_키워드'] = ', '.join(matched_keywords)
                                post_data['키워드_개수'] = len(matched_keywords)
                                post_data['갤러리'] = gallery_id

                                self.results.append(post_data)
                                page_pain_points += 1
                            else:
                                print(f"      ✗ 키워드 없음 → 건너뜀")

                        # 서버 부하 방지
                        time.sleep(1)

                    except Exception as e:
                        print(f"      ✗ 게시글 처리 오류: {e}")
                        continue

                # 목표 달성 확인
                current_total = len([r for r in self.results if r.get('갤러리') == gallery_id])
                if current_total >= target_pain_points:
                    print(f"\n✓ 목표 달성! 크롤링 종료")
                    break

                # 페이지 간 딜레이
                time.sleep(1.5)

            except Exception as e:
                print(f"  ✗ 페이지 {page} 크롤링 오류: {e}")
                continue

        final_count = len([r for r in self.results if r.get('갤러리') == gallery_id])
        print(f"\n'{gallery_id}' 크롤링 완료: {final_count}개 Pain Point 발견")

    def _extract_post_content(self, url, title, gallery_id):
        """게시글 본문 추출"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 본문 추출
            content = ''

            # 시도 1: div.write_div (일반 게시글)
            content_elem = soup.select_one('div.write_div')
            if content_elem:
                content = content_elem.get_text(strip=True)

            # 시도 2: div.writing_view_box
            if not content:
                content_elem = soup.select_one('div.writing_view_box')
                if content_elem:
                    content = content_elem.get_text(strip=True)

            # 본문이 너무 짧으면 무시
            if not content or len(content) < 10:
                print(f"      ✗ 본문 추출 실패 (너무 짧음: {len(content)}자)")
                return None

            # 본문 정제
            cleaned_content = self._clean_text(content)

            # 날짜 추출
            date_str = self._extract_date(soup)

            # 조회수 추출
            views = self._extract_views(soup)

            return {
                '날짜': date_str,
                '제목': title,
                '본문': cleaned_content,  # 정제된 본문
                '본문_전체_길이': len(content),
                '조회수': views,
                '링크': url,
            }

        except Exception as e:
            print(f"      ✗ 게시글 추출 오류: {e}")
            return None

    def _extract_date(self, soup):
        """날짜 추출"""
        try:
            date_elem = soup.select_one('span.gall_date')
            if date_elem:
                return date_elem.get_text(strip=True)
            return datetime.now().strftime('%Y.%m.%d')
        except:
            return datetime.now().strftime('%Y.%m.%d')

    def _extract_views(self, soup):
        """조회수 추출"""
        try:
            views_elem = soup.select_one('span.gall_count')
            if views_elem:
                return views_elem.get_text(strip=True)
            return '0'
        except:
            return '0'

    def _clean_text(self, text):
        """텍스트 정제 (CSV 가독성 향상)"""
        import re

        # 1. 줄바꿈을 공백으로 치환
        text = text.replace('\n', ' ').replace('\r', ' ')

        # 2. 탭을 공백으로 치환
        text = text.replace('\t', ' ')

        # 3. 연속된 공백을 하나로
        text = re.sub(r'\s+', ' ', text)

        # 4. 앞뒤 공백 제거
        text = text.strip()

        # 5. 길이 제한 (150자)
        if len(text) > 150:
            text = text[:150] + '...'

        return text

    def _find_pain_keywords(self, text):
        """Pain Point 키워드 찾기"""
        matched = []
        text_lower = text.lower()

        for keyword in self.keywords:
            if keyword in text_lower or keyword in text:
                matched.append(keyword)

        return list(set(matched))

    def save_to_csv(self, filename=None):
        """CSV 저장"""
        if not self.results:
            print("\n저장할 데이터가 없습니다.")
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'dc_pain_points_{timestamp}.csv'

        print(f"\n=== CSV 파일 저장 중 ===")

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['날짜', '갤러리', '제목', '본문', '본문_전체_길이', '조회수', '링크', '매칭_키워드', '키워드_개수']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.results:
                writer.writerow(row)

        print(f"✓ 저장 완료: {filename}")
        print(f"  - 총 {len(self.results)}개 항목")

        # 통계 저장
        stats_filename = filename.replace('.csv', '_통계.csv')
        self._save_statistics_csv(stats_filename)

        return filename

    def _save_statistics_csv(self, filename):
        """통계 CSV 저장"""
        all_keywords = []
        for result in self.results:
            keywords = [k.strip() for k in result['매칭_키워드'].split(',')]
            all_keywords.extend(keywords)

        keyword_counts = Counter(all_keywords)

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['키워드', '빈도수'])
            for keyword, count in keyword_counts.most_common():
                writer.writerow([keyword, count])

        print(f"✓ 통계 저장 완료: {filename}")

    def show_statistics(self):
        """통계 출력"""
        if not self.results:
            print("\n통계를 생성할 데이터가 없습니다.")
            return

        print("\n" + "="*60)
        print("📊 디시인사이드 Pain Point 통계")
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

        # 갤러리별 통계
        gallery_counts = Counter([r.get('갤러리', '') for r in self.results])
        print(f"\n📁 갤러리별 발견 개수:")
        for gallery, count in gallery_counts.items():
            print(f"  {gallery}: {count}개")

        # 본문 길이 통계
        total_length = sum([r['본문_전체_길이'] for r in self.results])
        avg_length = total_length / len(self.results) if self.results else 0
        print(f"\n📝 본문 길이:")
        print(f"  평균: {avg_length:.0f}자")
        print(f"  총합: {total_length:,}자")


def main():
    """메인 실행 함수"""
    print("="*60)
    print("🔍 Pain Point Finder - 디시인사이드 크롤러")
    print("="*60)

    # 갤러리 선택
    print("\n[1단계] 갤러리 선택")
    print("-" * 60)
    print("추천 갤러리:")
    print("  - baseball_new11: 국내야구")
    print("  - stock: 주식")
    print("  - dcbest: DCbest")
    print("  - hit: 힛갤")

    gallery_input = input("\n갤러리 ID 입력 (Enter=baseball_new11): ").strip()
    gallery_id = gallery_input if gallery_input else 'baseball_new11'

    # 키워드 설정
    print("\n[2단계] 키워드 설정")
    print("-" * 60)
    print("옵션:")
    print("  1. 기본 키워드 사용 (불편, 힘들어, 짜증 등 39개)")
    print("  2. 사용자 지정 키워드만 사용")
    print("  3. 기본 키워드 + 추가 키워드")

    keyword_option = input("\n선택 (Enter=1): ").strip()

    custom_keywords = None

    if keyword_option == '2':
        print("\n키워드를 쉼표(,)로 구분해서 입력하세요.")
        print("예: 힘들어,짜증,불편,ㅠㅠ")
        keyword_input = input("키워드: ").strip()
        if keyword_input:
            custom_keywords = [k.strip() for k in keyword_input.split(',')]
            print(f"✓ {len(custom_keywords)}개 키워드 설정")

    elif keyword_option == '3':
        print("\n추가할 키워드를 쉼표(,)로 구분해서 입력하세요.")
        keyword_input = input("추가 키워드: ").strip()
        if keyword_input:
            additional = [k.strip() for k in keyword_input.split(',')]
            custom_keywords = DCInsidePainPointCrawler.PAIN_POINT_KEYWORDS + additional
            print(f"✓ 기본 + 추가 = {len(custom_keywords)}개 키워드")

    # 설정
    print("\n[3단계] 크롤링 설정")
    print("-" * 60)

    pages_input = input("최대 페이지 수 (Enter=5): ").strip()
    max_pages = int(pages_input) if pages_input else 5

    target_input = input("목표 Pain Point 개수 (Enter=10): ").strip()
    target_points = int(target_input) if target_input else 10

    # 크롤링 시작
    print("\n" + "="*60)
    print("🚀 크롤링 시작!")
    print(f"💡 키워드 있는 게시글 {target_points}개를 찾을 때까지 탐색합니다")
    print("="*60)

    crawler = DCInsidePainPointCrawler(custom_keywords=custom_keywords)
    crawler.search_gallery(gallery_id, max_pages=max_pages, target_pain_points=target_points)

    # 결과 확인
    if not crawler.results:
        print("\n❌ Pain Point를 발견하지 못했습니다.")
        print("다른 갤러리나 설정을 시도해보세요.")
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
        print("\n💡 CSV 파일을 Excel이나 메모장으로 열 수 있습니다!")
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

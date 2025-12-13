#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
디시인사이드 HTML 구조 확인
"""

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://gall.dcinside.com/board/lists/?id=parenting"

print(f"URL: {url}")

response = requests.get(url, headers=headers, timeout=10)
print(f"응답 코드: {response.status_code}")
print(f"응답 길이: {len(response.text)}자")

# HTML 저장
with open('dc_response.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("\n✓ dc_response.html 저장 완료")
print("\n처음 1000자:")
print(response.text[:1000])

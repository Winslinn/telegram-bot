import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

http_page = requests.get('https://bbc.com', headers=headers)
soup = BeautifulSoup(http_page.content, "html.parser")
title = soup.title.string

payload = {
    "source_url": 'https://bbc.com',
    "title": title,
    "content": soup.get_text()
}

requests.get('http://192.168.0.187:5678/webhook-test/new-source', json=payload, headers=headers)
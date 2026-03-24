import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dataclasses import dataclass

@dataclass
class WebPage:
    url: str
    content: str
    links: List[str]

class SwarmCrawler:
    def __init__(self, seed_urls: List[str], num_workers: int):
        self.seed_urls = seed_urls
        self.num_workers = num_workers
        self.pages = []
        self.frontier = seed_urls
        self.visited = set()

    def crawl(self):
        while self.frontier:
            worker_tasks = [self.frontier.pop() for _ in range(min(self.num_workers, len(self.frontier)))]
            results = [self.crawl_page(url) for url in worker_tasks]
            self.pages.extend(results)
            self.visited.update(worker_tasks)
            self.frontier.extend([link for page in results for link in page.links if link not in self.visited])

    def crawl_page(self, url: str) -> WebPage:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        return WebPage(url, response.text, links)

if __name__ == '__main__':
    seed_urls = ['https://www.example.com', 'https://www.wikipedia.org']
    crawler = SwarmCrawler(seed_urls, num_workers=10)
    crawler.crawl()
    for page in crawler.pages:
        print(f'URL: {page.url}')
        print(f'Links: {page.links}')

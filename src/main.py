import os
import time
import random
import logging
from typing import List
from dataclasses import dataclass

from swarm_utils import (
    SwarmNode,
    SwarmMessage,
    SwarmMessageType,
    SwarmTaskManager
)

@dataclass
class CrawlTask:
    url: str
    depth: int

class DistributedCrawler:
    def __init__(self, swarm_nodes: List[SwarmNode]):
        self.swarm_nodes = swarm_nodes
        self.task_manager = SwarmTaskManager(swarm_nodes)
        self.logger = logging.getLogger(__name__)

    def crawl(self, start_urls: List[str], max_depth: int):
        tasks = [CrawlTask(url, 0) for url in start_urls]
        self.task_manager.submit_tasks(tasks)

        while True:
            task = self.task_manager.get_next_task()
            if not task:
                break

            self.logger.info(f'Crawling: {task.url} (depth {task.depth})')
            time.sleep(random.uniform(0.1, 1.0))  # Simulating crawling

            if task.depth < max_depth:
                new_tasks = [CrawlTask(f'{task.url}/page{i}', task.depth + 1) for i in range(3)]
                self.task_manager.submit_tasks(new_tasks)

        self.logger.info('Crawling complete.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Example usage
    swarm_nodes = [
        SwarmNode('node1', ['192.168.1.100', '192.168.1.101']),
        SwarmNode('node2', ['192.168.1.102', '192.168.1.103']),
        SwarmNode('node3', ['192.168.1.104', '192.168.1.105'])
    ]

    crawler = DistributedCrawler(swarm_nodes)
    crawler.crawl(['https://example.com', 'https://another-example.com'], max_depth=2)

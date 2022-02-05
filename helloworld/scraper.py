import time
from bs4 import BeautifulSoup
from collections import namedtuple
import requests
from urllib.parse import urlparse, urljoin


Link = namedtuple("Link", ["url", "name"])


class Scraper:
    def __init__(self, startpage):
        self._startpage = startpage if "https://" in startpage else "https://"+startpage
        self._unvisited = [startpage]
        self._visited = []
        self._domain = self._extract_hostname()

    def traverse(self):
        for page in self._pages_to_visit():
            html = self._get_content(page)

            soup = BeautifulSoup(html, 'html.parser')
            full_links = []
            for link in soup.find_all('a'):
                parsed = urlparse(link.get('href'))
                if not parsed.scheme:
                    # if scheme empty than url is probably path
                    url = urljoin(page, parsed.path)
                else:
                    # normal url or dead
                    url = link.get('href')
                full_links.append(Link(url, link.text))
            # TODO: yield page with full_links so service can build nodes map
            yield page, full_links
            self._update_unvisited(full_links)

    def _update_unvisited(self, links):
        links, _ = tuple(zip(*links))
        links = filter(lambda x: x not in self._visited, links)
        self._unvisited.extend(links)
        self._unvisited = list(set(self._unvisited))

    def _pages_to_visit(self):
        while self._unvisited:
            next_page = self._unvisited.pop()
            yield next_page
            self._visited.append(next_page)

    def _extract_hostname(self):
        domain = urlparse(self._startpage).hostname
        domain = '.'.join(domain.split('.')[-2:])
        return domain

    @staticmethod
    def _get_content(address) -> str:
        for i in range(3):
            try:
                r = requests.get(address)
            except requests.exceptions.ConnectionError:
                continue
            if r.status_code != 200:
                # TODO: think about including history (redirect)
                time.sleep(i*.5)
            else:
                return r.text
        else:
            return ""

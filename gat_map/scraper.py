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
        """Generator yielding page with outlinks
        :returns (page_url, [out_link_url], is_dead)"""
        for page in self._pages_to_visit():
            html = self._get_content(page)
            if html:
                is_dead = False
            else:
                is_dead = True
            soup = BeautifulSoup(html, 'html.parser')
            domain_links = []
            full_links = []
            for link in soup.find_all('a'):
                parsed = urlparse(link.get('href'))
                if not parsed.scheme:
                    # if scheme empty than url is probably path
                    url = urljoin(page, parsed.path)
                else:
                    # normal url or dead
                    url = link.get('href')
                # exclude external links for traversing
                if self._domain in urlparse(url).netloc:
                    path = urlparse(url).path
                    # exclude files besides html
                    if '.' not in path or path.split('.')[-1] in ['html', '']:
                        domain_links.append(Link(url, link.text))
                full_links.append(Link(url, link.text))
            yield page, full_links, is_dead
            self._update_unvisited(domain_links)

    def _update_unvisited(self, links):
        if links:
            links, _ = tuple(zip(*links))
            links = filter(lambda x: self._domain in urlparse(x).netloc, links)
            links = filter(lambda x: x not in self._visited, links)
            self._unvisited.extend(links)
            self._unvisited = list(set(self._unvisited))

    def _pages_to_visit(self):
        while self._unvisited:
            next_page = self._unvisited.pop()
            self._visited.append(next_page)
            yield next_page

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

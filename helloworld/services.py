from scraper import Scraper
from models import node_dao


def build_map(url):
    scr = Scraper(url)
    for url, links, is_dead in scr.traverse():
        node_dao.add_new(url, links, is_dead)
        node_dao.save_to_db()


if __name__ == '__main__':
    build_map("https://www.globalapptesting.com")

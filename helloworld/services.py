from helloworld.scraper import Scraper
from helloworld.models import node_dao
from helloworld.graph import GraphAnalyzer


def browse_page(url) -> None:
    """Create spider that walks through page and save all traversed links into db"""
    scr = Scraper(url)
    for url, links, is_dead in scr.traverse():
        node_dao.add_new(url, links, is_dead)
        node_dao.save_to_db()


def create_analyst() -> GraphAnalyzer:
    """Creates graph analyst from nodes that are in db"""
    analyst = GraphAnalyzer(node_dao.get_all())
    return analyst


def analyze_page(url) -> GraphAnalyzer:
    """Browses page and creates graph analyst after traversing links"""
    browse_page(url)
    return create_analyst()


def upload_nodes(json_file_path) -> GraphAnalyzer:
    """Load nodes from json file into db"""
    node_dao.load_from_db(json_file_path)
    return create_analyst()


def download_db():
    """Return path to db object for download"""
    return node_dao.db_copy()

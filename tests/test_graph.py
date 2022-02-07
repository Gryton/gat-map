import pytest
import json
import os
from helloworld.graph import GraphAnalyzer


@pytest.fixture
def analyzer():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    db_url = os.path.join(test_dir, "test.json")
    with open(db_url) as f:
        nodes = json.load(f)
    ga = GraphAnalyzer(nodes)
    return ga


def test_dead_links(analyzer):
    dead_links = analyzer.get_dead_links("globalapptesting.com")
    assert len(dead_links) == 10


def test_ext_links_count(analyzer):
    count = analyzer.average_number_of_external("globalapptesting.com")
    assert 20 < count < 21


def test_int_links_count(analyzer):
    count = analyzer.average_number_of_internal_links("globalapptesting.com")
    assert 95 < count < 96


def test_shortest_path(analyzer):
    path = analyzer.get_shortest_path('https://www.globalapptesting.com',
                                      'https://www.globalapptesting.com/blog/announcing-iso-27001-certification')
    assert 'https://www.globalapptesting.com/news' in path


def test_most_distant(analyzer):
    urls = analyzer.most_distant_subpages('https://www.globalapptesting.com')
    assert 'https://www.globalapptesting.com/blog/page/0' in urls
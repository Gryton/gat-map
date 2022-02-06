from helloworld.scraper import Scraper, Link
import pytest


@pytest.mark.parametrize("startpage,domain", [("https://www.globaltestingapp.com", "globaltestingapp.com"),
                                              ("www.globaltestingapp.com", "globaltestingapp.com")])
def test_domain_extraction(startpage, domain):
    scr = Scraper(startpage)
    assert scr._domain == domain


@pytest.mark.parametrize("visited,links,unvisited",
                         [(("https://www.globaltestingapp.com", "https://www.globaltestingapp.com/sth"),
                           (Link("https://www.globaltestingapp.com", ""),
                            Link("https://www.globaltestingapp.com/new", ""),
                            Link("javascript;", ""),
                            Link("'https://go.globalapptesting.com/hubfs/Marketing/content/Case%20Study/"
                                 "LiveSafe%20-%20Case%20Study.pdf';", "")),
                           ["https://www.globaltestingapp.com/new"]
                           )]
                         )
def test_filtering_unvisited_links(visited, links, unvisited):
    scr = Scraper("https://www.globaltestingapp.com")
    scr._visited = visited
    scr._unvisited = []
    scr._update_unvisited(links)
    assert set(scr._unvisited) == set(unvisited)


def test_traverse(mocker):
    scr = Scraper("https://www.sth.com")
    mocked_html = '<!doctype html><html class="no-js" lang="en">' \
                  '<a href="https://www.sth.com">Main</a>' \
                  '<a href="https://www.sth.com/sth">Sth</a>'\
                  '<a href="/New">New</a>'\
                  '</html>'
    mocker.patch('helloworld.scraper.Scraper._get_content', return_value=mocked_html)
    items = [item for item in scr.traverse()]
    assert set(scr._visited) == {"https://www.sth.com", "https://www.sth.com/sth", "https://www.sth.com/New"}
    assert ("https://www.sth.com/New", [("https://www.sth.com", "Main"),
                                        ("https://www.sth.com/sth", "Sth"),
                                        ("https://www.sth.com/New", "New")], False) in items

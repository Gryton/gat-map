import helloworld.models as models
import os
import pytest


test_db_url = 'test_models.json'


@pytest.fixture
def db(mocker):
    mocker.patch.object(models, 'db_url', test_db_url)
    yield
    os.remove(test_db_url)


def test_save_load(db):
    print(db)
    n1 = models.Node("https://www.sth.com/New", [("https://www.sth.com", "Main")], False)
    n2 = models.Node("https://www.sth.com/Sth", [("https://www.sth.com/s", "s")], False)
    nodes = [n1, n2]
    node_dao = models.NodeDAO(models.Node)
    node_dao.nodes = nodes
    node_dao.save_to_db()
    node_dao.load_from_db()
    assert node_dao.nodes[0].url == n1.url
    assert node_dao.nodes[1].url == n2.url


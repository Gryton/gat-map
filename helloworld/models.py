from typing import List, Tuple
import json

db_url = "tmp.json"


class Node:
    url: str
    outlinks: List[Tuple[str, str]]
    is_dead: bool

    def __init__(self, url, links, is_dead):
        self.url = url
        self.outlinks = links
        self.is_dead = is_dead


class NodeDAO:
    nodes = List[Node]

    def __init__(self, model):
        # model shall be used if switching to sqlalchemy and querying db
        self.model = model
        self.nodes = []

    def load_from_db(self):
        with open(db_url) as f:
            decoded = json.load(f)
        self.nodes = [Node(n['url'], n['links'], n['is_dead']) for n in decoded]

    def save_to_db(self):
        dump = [{'url': n.url, 'links': n.outlinks, 'is_dead': n.is_dead} for n in self.nodes]
        with open(db_url, 'w+') as f:
            json.dump(dump, f)

    def add_new(self, url, links, is_dead):
        node = Node(url, links, is_dead)
        self.nodes.append(node)


node_dao = NodeDAO(Node)

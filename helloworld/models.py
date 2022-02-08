from typing import List, Tuple
import json

db_url = "db.json"


class Node:
    url: str
    links: List[Tuple[str, str]]
    is_dead: bool

    def __init__(self, url, links, is_dead):
        self.url = url
        self.links = links
        self.is_dead = is_dead

    def __getitem__(self, item):
        if item == 'url':
            return self.url
        if item == 'links':
            return self.links
        if item == 'is_dead':
            return self.is_dead


class NodeDAO:
    nodes = List[Node]

    def __init__(self, model):
        # model shall be used if switching to sqlalchemy and querying db
        self.model = model
        self.nodes = []

    def load_from_db(self, json_file_path=None):
        if json_file_path:
            # TODO: file should be validated it is ok
            with open(json_file_path) as f:
                decoded = json.load(f)
        else:
            with open(db_url) as f:
                decoded = json.load(f)
        self.nodes = [Node(n['url'], n['links'], n['is_dead']) for n in decoded]

    def save_to_db(self):
        dump = [{'url': n.url, 'links': n.links, 'is_dead': n.is_dead} for n in self.nodes]
        with open(db_url, 'w+') as f:
            json.dump(dump, f)

    def add_new(self, url, links, is_dead):
        node = Node(url, links, is_dead)
        self.nodes.append(node)

    def get_all(self):
        if not self.nodes:
            self.load_from_db()
        return self.nodes

    @staticmethod
    def db_copy():
        """Returns path to db copy that can be downloaded"""
        return db_url


node_dao = NodeDAO(Node)

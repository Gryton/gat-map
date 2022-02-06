import networkx as nx
from typing import Dict, List, Optional
from urllib.parse import urlparse
from statistics import mean
import json


class GraphAnalyzer:
    def __init__(self, nodes: List[Dict]):
        self.nodes = nodes
        self.graph = self._create_graph()
        self.shortest_paths = nx.shortest_path(self.graph)

    def _create_graph(self):
        DG = nx.DiGraph()
        for n in self.nodes:
            DG.add_node(n["url"])
            for link in n["links"]:
                DG.add_node(link[0])
                DG.add_edge(n["url"], link[0])
        return DG

    def average_number_of_internal_links(self, domain):
        ext_counts = []
        for node in self.nodes:
            ext_count = len([link for link in node['links'] if domain in urlparse(link).netloc])
            ext_counts.append(ext_count)
        return mean(ext_counts)

    def average_number_of_external(self, domain):
        ext_counts = []
        for node in self.nodes:
            ext_count = len([link for link in node['links'] if domain not in urlparse(link).netloc])
            ext_counts.append(ext_count)
        return mean(ext_counts)

    def most_distant_subpages(self, source='https://globalapptesting.com', hops=Optional[int]):
        """Finds most distant subpage to reach from specified source. If number of hops is specified finds pages reachable
        with such number of hops

        :returns list of urls, number of hops"""
        paths = self.shortest_paths
        if hops is None:
            max_url = max(paths, key=lambda i: len(paths[i]))
            hops = len(paths[max_url])
        return [target for target in paths if len(paths[target]) == hops]

    def most_difficult_to_enter_pages(self):
        hubs, authorities = nx.hits(self.graph)
        values = [v for v in authorities.values() if v > 0]
        min_authority = min(values)
        difficult = [link for link in authorities if authorities[link] == min_authority]
        return difficult

    def most_linked_pages(self):
        hubs, authorities = nx.hits(self.graph)
        max_authority = max(authorities.values())
        most_linked = [link for link in authorities if authorities[link] == max_authority]
        return most_linked


if __name__ == '__main__':
    db_url = "tmp_copy.json"
    with open(db_url) as f:
        decoded = json.load(f)
    links_only = []
    for node in decoded:
        links = [el[0] for el in node["links"] if 'globalapptesting.com' in el[0]]
        if links:
            links_only.append(links)
    navigation_group = set.intersection(*map(set, links_only))

    DG = nx.DiGraph()
    # DG.add_node("Navigation")
    # for link in navigation_group:
    #     DG.add_node(f" {link}")
    #     DG.add_edge("Navigation", f" {link}")
    for n in decoded:
        DG.add_node(n["url"])
        for link in n["links"]:
            if link[0] in navigation_group:
                pass
            else:
                DG.add_node(link[0])
                DG.add_edge(n["url"], link[0])
    paths = nx.shortest_path(DG)
    path = nx.shortest_path(DG, 'https://www.globalapptesting.com', 'https://www.globalapptesting.com/blog/announcing-iso-27001-certification')
    pass
    # nx.draw(DG)
    # net = Network(notebook=False)
    # net.from_nx(DG)
    # net.show("example.html")

import networkx as nx
from typing import Dict, List, Optional
from urllib.parse import urlparse
from statistics import mean


class GraphAnalyzer:
    def __init__(self, nodes=None):
        self.nodes = nodes
        self.graph = self._create_graph()
        self.shortest_paths = nx.shortest_path(self.graph)

    def _create_graph(self):
        """Creates Directed Graph from nodes"""
        DG = nx.DiGraph()
        for n in self.nodes:
            DG.add_node(n["url"])
            for link in n["links"]:
                DG.add_node(link[0])
                DG.add_edge(n["url"], link[0])
        return DG

    def save(self):
        return nx.readwrite.node_link_data(self.graph)

    def average_number_of_internal_links(self, domain):
        """Counts all links in all nodes that have same domain as specified"""
        ext_counts = []
        for node in self.nodes:
            ext_count = len([link for link in node['links'] if domain in urlparse(link[0]).netloc])
            ext_counts.append(ext_count)
        return mean(ext_counts)

    def average_number_of_external(self, domain):
        """Counts all links in all nodes that have different domain then specified"""
        ext_counts = []
        for node in self.nodes:
            ext_count = len([link for link in node['links'] if domain not in urlparse(link[0]).netloc])
            ext_counts.append(ext_count)
        return mean(ext_counts)

    def most_distant_subpages(self, source='https://globalapptesting.com', hops: Optional[int] = None):
        """Finds most distant subpage to reach from specified source. If number of hops is specified finds pages
        reachable with such number of hops

        :returns list of urls, number of hops"""
        paths = self.shortest_paths[source]
        if hops is None:
            max_url = max(paths, key=lambda i: len(paths[i]))
            hops = len(paths[max_url])
        return [target for target in paths if len(paths[target]) == hops]

    def most_difficult_to_enter_pages(self):
        """Analyses graph with HITS algorithm and returns list of links that are linked the least"""
        hubs, authorities = nx.hits(self.graph)
        values = [v for v in authorities.values() if v > 0]
        min_authority = min(values)
        difficult = [link for link in authorities if authorities[link] == min_authority]
        return difficult

    def most_linked_pages(self):
        """Analyses graph with HITS algorithm and returns list of links that are linked the most"""
        hubs, authorities = nx.hits(self.graph)
        max_authority = max(authorities.values())
        most_linked = [link for link in authorities if authorities[link] == max_authority]
        return most_linked

    def get_dead_links(self, domain):
        """Returns list of dead links assigning them by is_dead equal to True"""
        dead_links = [node["url"] for node in self.nodes
                      if node["is_dead"] is True and domain in urlparse(node["url"]).netloc]
        return dead_links

    def get_shortest_path(self, source, target):
        """Returns shortest path from source to target in form of list with links in path"""
        return nx.shortest_path(self.graph, source, target)

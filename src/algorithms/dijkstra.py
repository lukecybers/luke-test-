"""
Shortest Path Dijkstra Algorithm Implementation.
Source: Standard Textbook Implementation.
"""
import sys
import heapq

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def dijkstra(self, src):
        # Min heap priority queue storing (distance, vertex)
        pq = []
        dist = [sys.maxsize] * self.V

        heapq.heappush(pq, (0, src))
        dist[src] = 0

        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue

            # Iterate through all adjacent vertices of u
            for v, weight in self.graph[u]:
                if dist[v] > dist[u] + weight:
                    dist[v] = dist[u] + weight
                    heapq.heappush(pq, (dist[v], v))

        return dist

def print_solution(dist):
    print("Vertex \tDistance from Source")
    for i in range(len(dist)):
        print(f"{i} \t\t{dist[i]}")

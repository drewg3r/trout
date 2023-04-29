import heapq


def yen_algorithm(graph: dict, start: int, end: int, k: int = 5):
    # Initialize the set of shortest paths
    shortest_paths = []

    # Initialize the heap with the initial path
    heap = [(0, [start])]

    # Loop until we have found k paths or the heap is empty
    while len(shortest_paths) < k and heap:
        # Pop the shortest path from the heap
        (cost, path) = heapq.heappop(heap)

        # Get the last vertex in the path
        node = path[-1]

        # If the last vertex is the end vertex, add the path to the set of shortest paths
        if node == end:
            shortest_paths.append(path)
        else:
            # Generate the potential new paths
            for neighbor, weight in graph[node].items():
                if neighbor not in path:
                    new_path = path + [neighbor]
                    new_cost = cost + min(weight)
                    heapq.heappush(heap, (new_cost, new_path))

    return shortest_paths


# funtion int int datetime
# class directions


# ordered dict,
#   key: station id(better station)
#   value:  datetime
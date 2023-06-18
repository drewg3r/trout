import heapq


def yen_algorithm(graph: dict, start: int, end: int, k: int = 5):
    # Initialize the set of shortest paths
    shortest_paths = []

    # Initialize the heap with the initial path
    heap = [(0, ([start], [None]))]

    # Loop until we have found k paths or the heap is empty
    while len(shortest_paths) < k and heap:
        # Pop the shortest path from the heap
        (cost, trip_data) = heapq.heappop(heap)
        path = trip_data[0]
        path_waypoint = trip_data[1]

        # Get the last vertex in the path
        node = path[-1]

        # If the last vertex is the end vertex, add the path to the set of shortest paths
        if node == end:
            shortest_paths.append((path, path_waypoint))
        else:
            # Generate the potential new paths
            for neighbor, trip_data in graph[node].items():
                if neighbor not in path:
                    weight = [e[0] for e in trip_data]
                    waypoints = [e[1] for e in trip_data]

                    new_cost = cost + min(weight)
                    new_path = path + [neighbor]
                    new_waypoint = waypoints[weight.index(min(weight))]
                    heapq.heappush(heap, (new_cost, (new_path, path_waypoint + [new_waypoint])))

    return shortest_paths

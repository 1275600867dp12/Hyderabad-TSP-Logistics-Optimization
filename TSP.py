"""
Travelling Salesman Problem (TSP) Case Study
Logistics Optimization in Hyderabad - Comparing Greedy vs Branch-and-Bound
Author: Vijay Durga Prasad
"""

import math
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------- DATASET ----------------------
locations = [
    "Gachibowli", "Madhapur", "Kondapur", "Kukatpally", "Hitech City",
    "Banjara Hills", "Secunderabad", "LB Nagar", "Charminar", "Begumpet"
]

# Distance matrix (approx. in km)
distance_matrix = [
    [0,5,4,10,3,12,15,18,14,11],
    [5,0,3,8,2,9,14,17,13,10],
    [4,3,0,7,2,11,13,16,12,9],
    [10,8,7,0,6,14,10,15,17,12],
    [3,2,2,6,0,10,13,16,12,9],
    [12,9,11,14,10,0,8,12,7,6],
    [15,14,13,10,13,8,0,14,9,5],
    [18,17,16,15,16,12,14,0,11,15],
    [14,13,12,17,12,7,9,11,0,8],
    [11,10,9,12,9,6,5,15,8,0]
]

# ---------------------- GREEDY ALGORITHM ----------------------
def tsp_greedy(distance_matrix, start=0):
    n = len(distance_matrix)
    visited = [False] * n
    path = [start]
    visited[start] = True
    total_distance = 0
    current = start

    for _ in range(n - 1):
        # Find nearest unvisited city
        next_city = min(
            [(distance_matrix[current][j], j) for j in range(n) if not visited[j]],
            key=lambda x: x[0]
        )[1]
        path.append(next_city)
        total_distance += distance_matrix[current][next_city]
        visited[next_city] = True
        current = next_city

    # Return to start city
    total_distance += distance_matrix[current][start]
    path.append(start)
    return path, total_distance

# ---------------------- BRANCH AND BOUND ----------------------
def tsp_branch_and_bound(distance_matrix, start=0):
    n = len(distance_matrix)
    best_path = []
    best_distance = math.inf

    def backtrack(path, visited, current_distance):
        nonlocal best_distance, best_path
        current_city = path[-1]

        # If all cities are visited, check total distance
        if len(path) == n:
            total_distance = current_distance + distance_matrix[current_city][start]
            if total_distance < best_distance:
                best_distance = total_distance
                best_path = path[:]
            return

        # Explore remaining cities
        for next_city in range(n):
            if not visited[next_city]:
                projected_distance = current_distance + distance_matrix[current_city][next_city]
                if projected_distance < best_distance:  # Pruning
                    visited[next_city] = True
                    path.append(next_city)
                    backtrack(path, visited, projected_distance)
                    path.pop()
                    visited[next_city] = False

    visited = [False] * n
    visited[start] = True
    backtrack([start], visited, 0)
    best_path.append(start)
    return best_path, best_distance

# ---------------------- VISUALIZATION ----------------------
def visualize_path(path, locations, title):
    G = nx.Graph()
    for i in range(len(path)-1):
        G.add_edge(locations[path[i]], locations[path[i+1]])

    plt.figure(figsize=(10,6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000,
            font_size=9, font_weight="bold", edge_color='gray')
    plt.title(title)
    plt.tight_layout()
    plt.show()

# ---------------------- MAIN EXECUTION ----------------------
if __name__ == "__main__":
    # Greedy algorithm execution
    greedy_path, greedy_distance = tsp_greedy(distance_matrix)
    print("\nGreedy Algorithm")
    print("Path:", " -> ".join([locations[i] for i in greedy_path]))
    print("Total Distance:", greedy_distance, "km")

    # Branch-and-Bound algorithm execution
    bb_path, bb_distance = tsp_branch_and_bound(distance_matrix)
    print("\nBranch & Bound Algorithm")
    print("Path:", " -> ".join([locations[i] for i in bb_path]))
    print("Total Distance:", bb_distance, "km")

    # Comparison graph
    plt.figure(figsize=(6,4))
    methods = ["Greedy", "Branch & Bound"]
    distances = [greedy_distance, bb_distance]
    plt.bar(methods, distances, color=['orange', 'green'])
    plt.title("Distance Comparison")
    plt.ylabel("Distance (km)")
    plt.show()

    # Visualize optimal route
    visualize_path(bb_path, locations, "Optimized Delivery Route (Branch & Bound)")

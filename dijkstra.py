# -*- coding: utf-8 -*-
"""
Created on Sat Dec 4 14:57:28 2024

@author: Biyuan Luo
"""
import json
import os # just for change the wd, won't be shown in the script

def json_to_adjacency_list(json_data):
    """
    Converting Json data to the adjacency list.
    
    Parameters:
        json_data: dict, JSON data containing city and connection information.

    Return:
        graph: dict, Adjacency list representation of a graph.
    """
    graph = {}
    connections = json_data["connections"]

    for connection in connections:
        from_city = connection["from"]
        to_city = connection["to"]
        weight = connection["weight"]

        if from_city not in graph:
            graph[from_city] = {}
        graph[from_city][to_city] = weight

        if to_city not in graph:
            graph[to_city] = {}
        graph[to_city][from_city] = weight

    return graph

def dijkstra(graph, start):
    """
    Dijkstra algorithm to find the shortest path from the start node to all other nodes.

    Parameters:
        graph: dict, adjacency list representation of the graph with weights.
                Example: {"A": {"B": 1, "C": 4}, "B": {"C": 2}, "C": {}}
        start: str, the starting node.

    Returns:
        S: The list of visited nodes
        Y: dict, the shortest path values to each node from the start.
        P: dict, the shortest path information to each node from the start.
    """
    S = []  # The visited node
    Y = {node: float('inf') for node in graph}  # Shortest path value, initially infinity
    P = {node: None for node in graph}  # path info

    Y[start] = 0

    while len(S) < len(graph):  # End when all nodes have been visited
        # The node with the smallest Y value is selected from the unvisited nodes
        current_node = min((node for node in graph if node not in S), key=lambda node: Y[node])
        S.append(current_node)  # 将当前节点加入已访问列表

        # Update Y and P of neighbor nodes
        for neighbor, weight in graph[current_node].items():
            if neighbor not in S:
                new_distance = Y[current_node] + weight
                if new_distance < Y[neighbor]:  # If find a shorter path
                    Y[neighbor] = new_distance
                    P[neighbor] = current_node  # update

    return S, Y, P


def reconstruct_path(P, start, end):
    """
    Reconstruct the path from the start to the end based on the path information.

    Parameters:
        P: dict, Path origin information.
        start: str, start city
        end: str, end city

    Return:
        path: str, Formatted path information（such as A -> B -> C）
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = P[current]
    path.reverse()
    return " -> ".join(path)


def print_shortest_paths(start_city, Y, P):
    """
    Prints the shortest path information from the starting point to all other nodes

    Parameters:
        start_city: str, start city
        Y: dict, Shortest path value from the starting point to each node
        P: dict, Path origin information.
    """
    for city, distance in Y.items():
        if city == start_city:
            continue  # omit start city
        path = reconstruct_path(P, start_city, city)
        print("--------------------------")
        print(f"Strat City: {start_city}")
        print(f"Destination City: {city}")
        print(f"Path Value: {distance} H")
        print(f"Path Info: {path}")
        print("--------------------------")


if __name__ == "__main__":
    # loading JSON file
    with open("city_network.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Convert to an adjacency list
    graph = json_to_adjacency_list(json_data)
    
    # test_1, start from Tromsø
    start_city1 = "Tromsø"
    S, Y, P = dijkstra(graph, start_city1)
    print_shortest_paths(start_city1, Y, P)
    
    # test_2, start from London
    start_city2 = "London"
    S, Y, P = dijkstra(graph, start_city2)
    print_shortest_paths(start_city2, Y, P)
    
    # test_3, start from Tromsø
    start_city3 = "Kyiv"
    S, Y, P = dijkstra(graph, start_city3)
    print_shortest_paths(start_city3, Y, P)
    
    # test_4, start from Tromsø
    start_city4 = "Baku"
    S, Y, P = dijkstra(graph, start_city4)
    print_shortest_paths(start_city4, Y, P)
    

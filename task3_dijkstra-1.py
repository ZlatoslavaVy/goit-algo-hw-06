from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


# ============================================================
# ЗАВДАННЯ 3: Алгоритм Дейкстри
# ============================================================

print("=" * 70)
print("ЗАВДАННЯ 3: Алгоритм Дейкстри - найкоротші шляхи")
print("=" * 70)

# Створення графа (той самий, що в завданні 1)
G = nx.Graph()

# Локації по країнах
ukraine = ["Київ", "Львів", "Одеса", "Харків"]
france = ["Париж", "Марсель", "Ліон"]
england = ["Лондон", "Манчестер", "Ліверпуль"]
usa = ["Нью-Йорк", "Лос-Анджелес", "Чикаго"]

# Додаємо всі вершини
all_locations = ukraine + france + england + usa
G.add_nodes_from(all_locations)

# Внутрішні дороги з вагами
ukraine_roads = [
    ("Київ", "Львів", 7), ("Київ", "Харків", 6), ("Київ", "Одеса", 6),
    ("Львів", "Одеса", 10), ("Харків", "Одеса", 9)
]

france_roads = [
    ("Париж", "Ліон", 5), ("Париж", "Марсель", 8), ("Ліон", "Марсель", 3)
]

england_roads = [
    ("Лондон", "Манчестер", 4), ("Лондон", "Ліверпуль", 4), ("Манчестер", "Ліверпуль", 1)
]

usa_roads = [
    ("Нью-Йорк", "Чикаго", 12), ("Чикаго", "Лос-Анджелес", 4), ("Нью-Йорк", "Лос-Анджелес", 5)
]

# Міжнародні рейси
international_flights = [
    ("Київ", "Париж", 3), ("Київ", "Лондон", 3), ("Львів", "Париж", 2),
    ("Париж", "Лондон", 1), ("Париж", "Нью-Йорк", 8), ("Лондон", "Нью-Йорк", 7),
    ("Одеса", "Марсель", 3)
]

# Додаємо ребра до графа
G.add_weighted_edges_from(ukraine_roads + france_roads + england_roads + usa_roads + international_flights)

print("\n" + "=" * 10)

# Масштабовані координати для візуалізації
scaled_coordinates = {
    "Лос-Анджелес": (5, 15), "Чикаго": (25, 25), "Нью-Йорк": (35, 22),
    "Ліверпуль": (50, 30), "Манчестер": (52, 28), "Лондон": (55, 22),
    "Париж": (65, 25), "Ліон": (70, 20), "Марсель": (72, 12),
    "Львів": (85, 25), "Київ": (95, 27), "Харків": (105, 26), "Одеса": (97, 15)
}

# Кольори для вершин
color_map = []
for node in G.nodes():
    if node in ukraine:
        color_map.append('#FFD700')
    elif node in france:
        color_map.append('#0055A4')
    elif node in england:
        color_map.append('#2D9D2E')
    elif node in usa:
        color_map.append('#B22234')

# Візуалізація графа
plt.figure(figsize=(18, 10))
pos = scaled_coordinates

nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color='gray')
nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=3000, edgecolors='black', linewidths=2)
nx.draw_networkx_labels(G, pos, font_size=11, font_weight='bold')

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)

plt.title('RPG World Map - Транспортна мережа', fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()


print("\n" + "=" * 30)

def dijkstra(graph, start):
    """Алгоритм Дейкстри для пошуку найкоротшого шляху"""
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    unvisited = list(graph.nodes())
    previous = {node: None for node in graph.nodes()}
    
    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current)
        
        if distances[current] == float('inf'):
            break
        
        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor]['weight']
            distance = distances[current] + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
    
    return distances, previous


def get_shortest_path(previous, start, goal):
    """Відновлення шляху з алгоритму Дейкстри"""
    path = []
    current = goal
    
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    return path if path[0] == start else None


def bfs(graph, start, goal):
    """Пошук у ширину (Breadth-First Search) - для порівняння"""
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == goal:
            return path
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    
    return None


# Знаходимо найкоротші шляхи з Києва до всіх міст
start_city = "Київ"
distances, previous = dijkstra(G, start_city)

print(f"\n🚀 Найкоротші шляхи з {start_city} до всіх міст (за часом):\n")

for city in sorted(distances.items(), key=lambda x: x[1]):
    if city[0] != start_city and distances[city[0]] != float('inf'):
        path = get_shortest_path(previous, start_city, city[0])
        print(f"{city[0]:15} - {distances[city[0]]:2.0f} год | Шлях: {' → '.join(path)}")

# Порівняння з BFS
print("\n" + "=" * 70)
print("ПОРІВНЯННЯ: BFS vs Алгоритм Дейкстри")
print("=" * 70)

goal_city = "Лос-Анджелес"
bfs_path = bfs(G, start_city, goal_city)
dijkstra_path = get_shortest_path(previous, start_city, goal_city)

# Рахуємо загальний час для BFS шляху
bfs_time = 0
for i in range(len(bfs_path) - 1):
    bfs_time += G[bfs_path[i]][bfs_path[i+1]]['weight']

dijkstra_time = distances[goal_city]

print(f"\nШлях з {start_city} до {goal_city}:\n")
print(f"BFS шлях:      {' → '.join(bfs_path)}")
print(f"Час: {bfs_time} годин\n")
print(f"Дейкстра шлях: {' → '.join(dijkstra_path)}")
print(f"Час: {dijkstra_time:.0f} годин")
print(f"\n✅ Алгоритм Дейкстри знайшов оптимальний шлях за часом!")

print("\n" + "=" * 70)
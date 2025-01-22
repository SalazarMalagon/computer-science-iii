import networkx as nx
import matplotlib.pyplot as plt
# Crear el gráfico dirigido para el cuarto lenguaje
# Crear el gráfico dirigido para el segundo lenguaje
G2 = nx.DiGraph()

# Agregar nodos y transiciones para el lenguaje (abc ∪ bca ∪ cab)(abc ∪ bca ∪ cab)*
# Estados q0, q1, q2, q3, q4 para manejar las transiciones
G2.add_edges_from([
    ("q0", "q1", {"label": "a"}),
    ("q1", "q2", {"label": "b"}),
    ("q2", "q3", {"label": "c"}),
    ("q0", "q4", {"label": "b"}),
    ("q4", "q1", {"label": "c"}),
    ("q4", "q2", {"label": "a"}),
    ("q0", "q5", {"label": "c"}),
    ("q5", "q6", {"label": "a"}),
    ("q6", "q7", {"label": "b"}),
    ("q3", "q0", {"label": "a"}),
    ("q3", "q1", {"label": "b"}),
    ("q3", "q4", {"label": "c"}),
])

# Posiciones de los nodos para visualización
pos2 = {
    "q0": (0, 0), "q1": (1, 1), "q2": (2, 1),
    "q3": (3, 1), "q4": (1, -1), "q5": (2, -1),
    "q6": (3, -1), "q7": (4, -1)
}

# Dibujar el grafo
plt.figure(figsize=(12, 6))
nx.draw_networkx(G2, pos2, with_labels=True, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold", arrows=True)
edge_labels2 = nx.get_edge_attributes(G2, "label")
nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color="red")
plt.title("Finite-State Machine for Language (abc ∪ bca ∪ cab)(abc ∪ bca ∪ cab)*")
plt.axis("off")
plt.show()

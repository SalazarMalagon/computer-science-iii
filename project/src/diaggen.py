import tkinter as tk
from tkinter import ttk
import sqlparse
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class diaggen:


    def parse_sql_file(sql_file):
        """Lee el archivo SQL y extrae las tablas y sus columnas."""
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_content = file.read()

        statements = sqlparse.split(sql_content)
        tables = {}

        for statement in statements:
            parsed = sqlparse.parse(statement)[0]
            tokens = [token for token in parsed.tokens if not token.is_whitespace]

            if tokens and tokens[0].ttype is None and tokens[0].value.upper() == "CREATE TABLE":
                table_name = tokens[2].get_real_name()
                columns = []

                inside_parens = False
                for token in tokens:
                    if token.value == "(":
                        inside_parens = True
                    elif token.value == ")":
                        inside_parens = False
                    elif inside_parens and token.ttype is None:
                        parts = token.value.split()
                        col_name = parts[0]
                        columns.append(col_name)

                tables[table_name] = columns

        return tables

    def draw_schema(tables):

        

        """Dibuja el diagrama relacional usando NetworkX y Matplotlib."""
        G = nx.DiGraph()
        
        # Añadir nodos (tablas)
        for table, columns in tables.items():
            G.add_node(table, label=f"{table}\n" + "\n".join(columns))

        # Añadir relaciones (si se detectan claves foráneas, aquí puedes mejorarlo)
        for table, columns in tables.items():
            for column in columns:
                if column.endswith("_id") and column[:-3] in tables:  # Asumimos convenciones tipo "autor_id"
                    G.add_edge(table, column[:-3])  # Relación detectada

        return G

    def plot_graph(G, root):
        """Muestra el diagrama en una ventana Tkinter."""
        fig, ax = plt.subplots(figsize=(6, 4))
        pos = nx.spring_layout(G)

        # Dibujar nodos y bordes
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10, ax=ax)

        # Agregar etiquetas con los nombres de los campos dentro de los nodos
        labels = nx.get_node_attributes(G, 'label')
        for node, (x, y) in pos.items():
            ax.text(x, y, labels[node], fontsize=9, ha="center", bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

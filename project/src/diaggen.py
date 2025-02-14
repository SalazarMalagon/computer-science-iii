import re
import networkx as nx
import matplotlib.pyplot as plt

class diaggen:
    def parse_sql_file(file_path):
        """
        Lee el archivo SQL, extrae las definiciones de tablas y relaciones de claves foráneas.
        
        Retorna un diccionario con:
        - 'tables': {nombre_tabla: [lista de definiciones (columnas/constraints)]}
        - 'foreign_keys': [(tabla, tabla_referenciada, columna_fk, columna_ref), ...]
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        tables = {}
        foreign_keys = []

        # 1. Procesar las sentencias CREATE TABLE
        pattern_create = re.compile(r'CREATE\s+TABLE\s+(\w+)\s*\((.*?)\);', re.DOTALL | re.IGNORECASE)
        tables_matches = pattern_create.findall(sql_script)

        for table_name, columns_str in tables_matches:
            # Separa las líneas (asumiendo que están separadas por comas)
            columns_lines = [line.strip() for line in columns_str.split(',') if line.strip()]
            tables[table_name] = columns_lines

            # Si hubiese claves foráneas inline en la definición, también se podrían extraer
            fk_pattern_inline = re.compile(
                r'FOREIGN\s+KEY\s*\(\s*([`"\w]+)\s*\)\s+REFERENCES\s+([`"\w]+)\s*\(\s*([`"\w]+)\s*\)', 
                re.IGNORECASE
            )
            for line in columns_lines:
                fk_match = fk_pattern_inline.search(line)
                if fk_match:
                    fk_column, ref_table, ref_column = fk_match.groups()
                    foreign_keys.append((table_name, ref_table, fk_column, ref_column))

        # 2. Procesar sentencias ALTER TABLE para claves foráneas
        pattern_alter = re.compile(
            r'ALTER\s+TABLE\s+(\w+).*?ADD\s+FOREIGN\s+KEY\s*\(\s*([`"\w]+)\s*\)\s+REFERENCES\s+(\w+)\s*\(\s*([`"\w]+)\s*\)',
            re.DOTALL | re.IGNORECASE
        )
        alter_matches = pattern_alter.findall(sql_script)

        for table_name, fk_column, ref_table, ref_column in alter_matches:
            # Si la tabla no se había agregado (por ejemplo, si solo aparece en ALTER), la agregamos vacía
            if table_name not in tables:
                tables[table_name] = []
            foreign_keys.append((table_name, ref_table, fk_column, ref_column))

        # Depuración: imprimir resultados
        print("Tablas encontradas:", list(tables.keys()))
        print("Claves foráneas encontradas:", foreign_keys)

        return {'tables': tables, 'foreign_keys': foreign_keys}

    def graficar_diagrama(sql_info, zoom_factor=1.0):
        """
        Dibuja el diagrama y permite ajustar el zoom modificando los límites del gráfico.
        El parámetro zoom_factor: 
        - Valores > 1 harán un "zoom in" (más cercano).
        - Valores < 1 harán un "zoom out" (más alejado).
        """
        tables = sql_info.get('tables', {})
        foreign_keys = sql_info.get('foreign_keys', [])

        G = nx.DiGraph()

        for table, atributos in tables.items():
            label = f"{table}\n" + "\n".join(atributos)
            G.add_node(table, label=label)

        for table, ref_table, fk_column, ref_column in foreign_keys:
            edge_label = f"{fk_column} → {ref_column}"
            G.add_edge(table, ref_table, label=edge_label)

        # Calcular posiciones
        pos = nx.spring_layout(G)

        # Dibujar nodos y etiquetas
        node_labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=3000)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='black')
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

        # Ajustar los límites del gráfico para aplicar el zoom
        # Obtenemos los valores x e y de todas las posiciones:
        x_values = [x for x, y in pos.values()]
        y_values = [y for x, y in pos.values()]

        # Calcular límites mínimos y máximos
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        # Calcular márgenes adicionales en función del zoom_factor
        x_margin = (x_max - x_min) * (1 - zoom_factor) / 2
        y_margin = (y_max - y_min) * (1 - zoom_factor) / 2

        plt.xlim(x_min - x_margin, x_max + x_margin)
        plt.ylim(y_min - y_margin, y_max + y_margin)

        plt.title("Diagrama de Tablas")
        plt.axis('off')
        plt.show()
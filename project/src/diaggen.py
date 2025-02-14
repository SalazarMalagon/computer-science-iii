import re
import networkx as nx
import matplotlib.pyplot as plt

class diaggen:
    def parse_sql_file(file_path):
        """
        Reads the SQL file, extracts table definitions and foreign key relationships.
        
        Returns a dictionary with:
        - 'tables': {table_name: [list of definitions (columns/constraints)]}
        - 'foreign_keys': [(table, referenced_table, fk_column, ref_column), ...]
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        tables = {}
        foreign_keys = []

        # 1. Process CREATE TABLE statements
        pattern_create = re.compile(r'CREATE\s+TABLE\s+(\w+)\s*\((.*?)\);', re.DOTALL | re.IGNORECASE)
        tables_matches = pattern_create.findall(sql_script)

        for table_name, columns_str in tables_matches:
            # Split lines (assuming they are separated by commas)
            columns_lines = [line.strip() for line in columns_str.split(',') if line.strip()]
            tables[table_name] = columns_lines

            # If there are inline foreign keys in the definition, they can also be extracted
            fk_pattern_inline = re.compile(
                r'FOREIGN\s+KEY\s*\(\s*([`"\w]+)\s*\)\s+REFERENCES\s+([`"\w]+)\s*\(\s*([`"\w]+)\s*\)', 
                re.IGNORECASE
            )
            for line in columns_lines:
                fk_match = fk_pattern_inline.search(line)
                if fk_match:
                    fk_column, ref_table, ref_column = fk_match.groups()
                    foreign_keys.append((table_name, ref_table, fk_column, ref_column))

        # 2. Process ALTER TABLE statements for foreign keys
        pattern_alter = re.compile(
            r'ALTER\s+TABLE\s+(\w+).*?ADD\s+FOREIGN\s+KEY\s*\(\s*([`"\w]+)\s*\)\s+REFERENCES\s+(\w+)\s*\(\s*([`"\w]+)\s*\)',
            re.DOTALL | re.IGNORECASE
        )
        alter_matches = pattern_alter.findall(sql_script)

        for table_name, fk_column, ref_table, ref_column in alter_matches:
            # If the table was not added before (e.g., if it only appears in ALTER), add it empty
            if table_name not in tables:
                tables[table_name] = []
            foreign_keys.append((table_name, ref_table, fk_column, ref_column))

        # Debugging: print results
        print("Tables found:", list(tables.keys()))
        print("Foreign keys found:", foreign_keys)

        return {'tables': tables, 'foreign_keys': foreign_keys}

    def graficar_diagrama(sql_info, zoom_factor=1.0):
        """
        Draws the diagram and allows zoom adjustment by modifying the graph limits.
        The zoom_factor parameter: 
        - Values > 1 will "zoom in" (closer view).
        - Values < 1 will "zoom out" (farther view).
        """
        tables = sql_info.get('tables', {})
        foreign_keys = sql_info.get('foreign_keys', [])

        G = nx.DiGraph()

        for table, attributes in tables.items():
            label = f"{table}\n" + "\n".join(attributes)
            G.add_node(table, label=label)

        for table, ref_table, fk_column, ref_column in foreign_keys:
            edge_label = f"{fk_column} → {ref_column}"
            G.add_edge(table, ref_table, label=edge_label)

        # Compute positions
        pos = nx.spring_layout(G)

        # Draw nodes and labels
        node_labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=3000)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='black')
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

        # Adjust graph limits to apply zoom
        # Get x and y values of all positions:
        x_values = [x for x, y in pos.values()]
        y_values = [y for x, y in pos.values()]

        # Compute min and max limits
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        # Compute additional margins based on zoom_factor
        x_margin = (x_max - x_min) * (1 - zoom_factor) / 2
        y_margin = (y_max - y_min) * (1 - zoom_factor) / 2

        plt.xlim(x_min - x_margin, x_max + x_margin)
        plt.ylim(y_min - y_margin, y_max + y_margin)

        plt.title("Table Diagram")
        plt.axis('off')
        plt.show()

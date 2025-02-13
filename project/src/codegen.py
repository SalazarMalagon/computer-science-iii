class CodeGenerator:
    def generate_sql(self, semantic_structure: dict) -> str:
        """Genera el código SQL (DDL) a partir de la estructura semántica.

        Args:
            semantic_structure (dict): Representación semántica con claves 'entities' y 'relationships'.

        Returns:
            str: Código SQL completo.
        """
        sql_lines = []
        entities = semantic_structure.get("entities", {})
        relationships = semantic_structure.get("relationships", {})

        # Generar CREATE TABLE para cada entidad
        for entity_name, info in entities.items():
            columns = []
            for attr in info["attributes"]:
                col_def = self._build_column_definition(attr, info["properties"][attr])
                columns.append(col_def)
            
            # Añadir PRIMARY KEY
            pk_attr = self._find_primary_key(info["properties"])
            if pk_attr:
                columns.append(f"PRIMARY KEY ({pk_attr})")
            
            create_table = f"CREATE TABLE {entity_name} (\n    " + ",\n    ".join(columns) + "\n);"
            sql_lines.append(create_table)

        # Generar claves foráneas para relaciones
        for rel_name, rel_info in relationships.items():
            origin = rel_info["origin"]
            destination = rel_info["destination"]
            pk_origin = self._find_primary_key(entities[origin]["properties"])
            
            if pk_origin:
                fk_statement = (
                    f"ALTER TABLE {destination} "
                    f"ADD COLUMN {origin}_id INT NOT NULL, "
                    f"ADD FOREIGN KEY ({origin}_id) REFERENCES {origin}({pk_origin});"
                )
                sql_lines.append(fk_statement)

        return "\n\n".join(sql_lines)

    def _build_column_definition(self, attr_name: str, properties: list) -> str:
        """Construye la definición de una columna SQL."""
        type_map = {
            "INT": "INT",
            "CHAR": "VARCHAR(255)"
        }
        
        constraints = []
        col_parts = [attr_name]
        
        # Determinar tipo de dato
        for prop in properties:
            if prop in type_map:
                col_parts.append(type_map[prop])
        
        # Añadir constraints
        if "NON_NULL" in properties:
            constraints.append("NOT NULL")
        if "AUT" in properties:
            constraints.append("AUTO_INCREMENT")
        
        # Combinar todo
        return " ".join(col_parts + constraints)

    def _find_primary_key(self, properties: dict) -> str:
        """Encuentra el atributo que es PRIMARY KEY."""
        for attr, props in properties.items():
            if "PK" in props:
                return attr
        return None
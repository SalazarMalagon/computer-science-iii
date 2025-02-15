class CodeGenerator:
    def generate_sql(self, semantic_data):
        sql_code = []
        entities = semantic_data.get('entities', {})
        relationships = semantic_data.get('relationships', [])

        # Generate CREATE TABLE for each entity
        for entity_name, attributes in entities.items():
            columns = []
            primary_keys = []
            for attr in attributes:
                # Determine data type and properties
                data_type = "INT" if "INT" in attr['properties'] else "VARCHAR(255)"
                constraints = []
                if "PK" in attr['properties']:
                    primary_keys.append(attr['name'])
                if "NON_NULL" in attr['properties']:
                    constraints.append("NOT NULL")
                if "AUT" in attr['properties'] and data_type == "INT":
                    constraints.append("AUTO_INCREMENT")
                
                column_def = f"{attr['name']} {data_type} {' '.join(constraints)}".strip()
                columns.append(column_def)
            
            # Add PRIMARY KEY clause
            if primary_keys:
                pk_clause = f"PRIMARY KEY ({', '.join(primary_keys)})"
                columns.append(pk_clause)
            
            create_table = f"CREATE TABLE {entity_name} (\n    " + ",\n    ".join(columns) + "\n);"
            sql_code.append(create_table)

        # Generate FOREIGN KEYS based on relationships
        for rel in relationships:
            entity1, entity2 = rel['entities']
            cardinality = rel['cardinality']
            
            # ONE_TO_MANY: FK in the "many" entity
            if cardinality == "ONE_TO_MANY":
                # Find PK of the "one" entity (entity1)
                pk_entity1 = next(attr['name'] for attr in entities[entity1] if "PK" in attr['properties'])
                fk_column = f"{entity1}_{pk_entity1}"
                
                # Add FK column if it does not exist
                if not any(attr['name'] == fk_column for attr in entities[entity2]):
                    sql_code.append(f"ALTER TABLE {entity2} ADD COLUMN {fk_column} INT;")
                
                # Add FOREIGN KEY constraint
                sql_code.append(
                    f"ALTER TABLE {entity2} ADD FOREIGN KEY ({fk_column}) "
                    f"REFERENCES {entity1}({pk_entity1});"
                )
            if cardinality == "MANY_TO_MANY":
                # Obtener los nombres de las claves primarias de ambas entidades
                pk_entity1 = next(attr['name'] for attr in entities[entity1] if "PK" in attr['properties'])
                pk_entity2 = next(attr['name'] for attr in entities[entity2] if "PK" in attr['properties'])

                # Crear el nombre de la tabla intermedia (convención: entidad1_entidad2)
                join_table = f"{entity1}_{entity2}"

                # Crear la tabla intermedia con las claves foráneas
                sql_code.append(f"CREATE TABLE {join_table} (")
                sql_code.append(f"    {entity1}_{pk_entity1} INT NOT NULL,")
                sql_code.append(f"    {entity2}_{pk_entity2} INT NOT NULL,")
                sql_code.append(f"    PRIMARY KEY ({entity1}_{pk_entity1}, {entity2}_{pk_entity2}),")
                sql_code.append(f"    FOREIGN KEY ({entity1}_{pk_entity1}) REFERENCES {entity1}({pk_entity1}),")
                sql_code.append(f"    FOREIGN KEY ({entity2}_{pk_entity2}) REFERENCES {entity2}({pk_entity2})")
                sql_code.append(f");")

            if cardinality == "ONE_TO_ONE":
                # Obtener las claves primarias de ambas entidades
                pk_entity1 = next(attr['name'] for attr in entities[entity1] if "PK" in attr['properties'])
                pk_entity2 = next(attr['name'] for attr in entities[entity2] if "PK" in attr['properties'])

                # Decidir en qué entidad agregar la clave foránea (puede ser entity2 en este caso)
                fk_column = f"{entity1}_{pk_entity1}"
                
                # Agregar la clave foránea en entity2 si no existe
                if not any(attr['name'] == fk_column for attr in entities[entity2]):
                    sql_code.append(f"ALTER TABLE {entity2} ADD COLUMN {fk_column} INT UNIQUE;")

                # Agregar la restricción de clave foránea
                sql_code.append(
                    f"ALTER TABLE {entity2} ADD FOREIGN KEY ({fk_column}) "
                    f"REFERENCES {entity1}({pk_entity1});"
                )


        return "\n\n".join(sql_code)

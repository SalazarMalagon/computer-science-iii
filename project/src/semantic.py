class SemanticAnalyzer:
    """Analizador semántico para validar entidades y relaciones."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.entities = {}  # Almacena entidades y sus atributos
        self.relationships = []  # Almacena relaciones
        self.errors = []  # Lista de errores semánticos

    def analyze(self):
        """Realiza el análisis semántico y devuelve los errores encontrados."""
        self._collect_definitions()
        self._validate_relationships()
        return self.errors

    def _collect_definitions(self):
        """Recopila entidades y relaciones del código."""
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.type_ == "KEYWORD":
                if token.value == "ENTITY":
                    self._process_entity(i + 1)
                elif token.value == "RELATIONSHIP":
                    self._process_relationship(i + 1)
            i += 1

    def _process_entity(self, start_index):
        entity_name = self.tokens[start_index].value
        self.entities[entity_name] = []
        i = start_index + 2  # Saltar ':' después del nombre
        
        while i < len(self.tokens) and self.tokens[i].value != ";":
            if self.tokens[i].type_ == "IDENTIFIER":
                attr = {
                    'name': self.tokens[i].value,
                    'properties': []
                }
                j = i + 2  # Saltar ':' después del nombre del atributo
                while j < len(self.tokens) and self.tokens[j].value not in (';', 'IDENTIFIER'):
                    if self.tokens[j].type_ == "PROPERTY":
                        attr['properties'].append(self.tokens[j].value)
                    j += 1
                self.entities[entity_name].append(attr)
                i = j
            else:
                i += 1

    def _validate_attribute(self, attr_name, entity_name, pos):
        """Valida que el atributo no esté duplicado."""
        existing_attrs = [attr["name"] for attr in self.entities[entity_name]]
        if attr_name in existing_attrs:
            self._add_error(f"Atributo duplicado: '{attr_name}' en entidad '{entity_name}'", pos)

    def _skip_attribute_properties(self, start_index):
        """Avanza hasta el final de las propiedades de un atributo."""
        i = start_index
        while i < len(self.tokens) and self.tokens[i].value != ";":
            if self.tokens[i].type_ == "SEPARATOR":
                i += 1
            else:
                i += 1
        return i

    def _process_relationship(self, start_index):
        """Procesa una definición de relación."""
        rel_name = self.tokens[start_index].value
        i = start_index + 2  # Saltar ':' después del nombre
        
        entity1 = self.tokens[i].value  # Primera entidad
        i += 2  # Saltar 'GO'
        entity2 = self.tokens[i].value  # Segunda entidad
        i += 2  # Saltar ':'
        cardinality = self.tokens[i].value  # Cardinalidad
        
        self.relationships.append({
            'name': rel_name,
            'entities': [entity1, entity2],
            'cardinality': cardinality
        })

    def _validate_relationships(self):
        """Valida que las entidades en relaciones existan."""
        for rel in self.relationships:
            # Acceder a las entidades desde el diccionario de la relación
            entity1 = rel['entities'][0]
            entity2 = rel['entities'][1]
            
            if entity1 not in self.entities:
                self._add_error(f"Entidad no definida en relación: '{entity1}'")
            if entity2 not in self.entities:
                self._add_error(f"Entidad no definida en relación: '{entity2}'")

    def _add_error(self, message, pos=None):
        """Agrega un error semántico con contexto."""
        if pos is not None and pos < len(self.tokens):
            token = self.tokens[pos]
            message += f" (Línea {token.line}, Columna {token.column})"
        self.errors.append(message)
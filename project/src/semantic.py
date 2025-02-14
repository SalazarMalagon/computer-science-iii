class SemanticAnalyzer:
    """Semantic analyzer to validate entities and relationships."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.entities = {}
        self.relationships = []
        self.errors = []

    def analyze(self):
        """Performs semantic analysis and returns any errors found."""
        self._collect_definitions()
        self._validate_relationships()
        return self.errors

    def _collect_definitions(self):
        """Collects entities and relationships from code."""
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
        """Processes an entity definition."""
        entity_name = self.tokens[start_index].value
        if entity_name in self.entities:
            self._add_error(f"Duplicate entity: '{entity_name}'", start_index)
        
        self.entities[entity_name] = []
        i = start_index + 2

        attributes = {}
        
        while i < len(self.tokens):
            # Skip empty commas, semicolons and colons
            if self.tokens[i].type_ in ("SEPARATOR", "SEMITERMINATOR"):
                i += 1
                continue
            
            # End of entity definition
            if self.tokens[i].type_ not in ("IDENTIFIER", "PROPERTY"):
                break
            
            # Process an attribute
            if self.tokens[i].type_ == "IDENTIFIER":
                attr_name = self.tokens[i].value
                i += 2
                
                properties = []
                while i < len(self.tokens) and self.tokens[i].type_ in ("PROPERTY", "SEPARATOR"):
                    if self.tokens[i].type_ == "PROPERTY":
                        properties.append(self.tokens[i].value)
                    i += 1
                
                # Validate and save the attribute
                self._validate_attribute(attr_name, entity_name, i)
                attributes[attr_name] = properties
                self._validate_attribute_properties(entity_name, properties)
                self.entities[entity_name].append({
                    "name": attr_name,
                    "properties": properties
                })
        self._validate_attribute_properties(entity_name, attributes)

    def _validate_attribute(self, attr_name, entity_name, pos):
        """Validates that the attribute is not duplicated."""
        existing_attrs = [attr["name"] for attr in self.entities[entity_name]]
        if attr_name in existing_attrs:
            self._add_error(f"Duplicate attribute: '{attr_name}' in entity '{entity_name}'", pos)

    def _validate_attribute_properties(self, entity, attributes):

        if "PK" in attributes and "NON_PK" in attributes:
            print(f"Error in {entity}: PK and NON_PK cannot coexist")

        if "NULL" in attributes and "NON_NULL" in attributes:
            print(f"Error in {entity}: NULL and NON_NULL cannot coexist.")
    
        if "AUT" in attributes and "NON_AUT" in attributes:
            print(f"Error in {entity}: AUT and NON_AUT cannot coexist.")


    def _skip_attribute_properties(self, start_index):
        """Move to the end of an attribute's properties."""
        i = start_index
        while i < len(self.tokens) and self.tokens[i].value != ";":
            if self.tokens[i].type_ == "SEPARATOR":
                i += 1
            else:
                i += 1
        return i

    def _process_relationship(self, start_index):
        """Process a relationship definition"""
        rel_name = self.tokens[start_index].value
        i = start_index + 2 
        
        entity1 = self.tokens[i].value  # First entity
        i += 2 
        entity2 = self.tokens[i].value  # Second entity
        i += 2 
        cardinality = self.tokens[i].value  # Cardinality
        
        self.relationships.append({
            'name': rel_name,
            'entities': [entity1, entity2],
            'cardinality': cardinality
        })

    def _validate_relationships(self):
        """Validates that entities in relationships exist."""
        for rel in self.relationships:
            # Accessing entities from the relation dictionary
            entity1 = rel['entities'][0]
            entity2 = rel['entities'][1]
            
            if entity1 not in self.entities:
                self._add_error(f"Entity not defined in relation to: '{entity1}'")
            if entity2 not in self.entities:
                self._add_error(f"Entity not defined in relation to: '{entity2}'")

    def _add_error(self, message, pos=None):
        """Add a semantic error with context."""
        if pos is not None and pos < len(self.tokens):
            token = self.tokens[pos]
            message += f" (Line {token.line}, Column {token.column})"
        self.errors.append(message)
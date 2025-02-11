# <S>                       -> <ENTITY_DEFINITION> | <RELATIONSHIP_DEFINITION>
# <ENTITY_DEFINITION>       -> "ENTITY" <IDENTIFIER> ":" <ATTRIBUTE_LIST>
# <ATTRIBUTE_LIST>          -> <ATTRIBUTE> | <ATTRIBUTE> "," <ATTRIBUTE_LIST>
# <ATTRIBUTE>               -> <IDENTIFIER> ":" <ATTRIBUTE_PROPERTIES>
# <ATTRIBUTE_PROPERTIES>    -> <PROPERTY> | <PROPERTY> "," <ATTRIBUTE_PROPERTIES>
# <PROPERTY>                -> "PK" | "NON_PK" | "NON_NULL" | "INT" | "CHAR" | "AUT" | "NON_AUT"

# <RELATIONSHIP_DEFINITION> -> "RELATIONSHIP" <IDENTIFIER> ":" <RELATION_DETAILS>
# <RELATION_DETAILS>        -> <IDENTIFIER> "GO" <IDENTIFIER> ":" <CARDINALITY>
# <CARDINALITY>             -> "ONE_TO_ONE" | "ONE_TO_MANY" | "MANY_TO_MANY"



class SintacticAnalyzer:
    """This class represents the behavior of a syntactic analyzer."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        """Avanza al siguiente token en la lista."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None  # Ya no hay más tokens

        # Asegurarnos de que no empieza en None
        if self.current_token is None and self.pos == 0:
            self.error("Empty token list, cannot parse")


    def parse(self):
        if not self.tokens:
            self.error("At least one ENTITY or RELATIONSHIP definition is required")

        print("Starting syntactic analysis...")
        while self.current_token and self.current_token.type_ == "KEYWORD" and self.current_token.value in ["ENTITY", "RELATIONSHIP"]:
            if self.current_token.value == "ENTITY":
                self.entity()
            elif self.current_token.value == "RELATIONSHIP":
                self.relationship()
            else:
                self.error("ENTITY or RELATIONSHIP")
        print("Syntactic analysis completed successfully!")


    def entity(self):
        """Parses an ENTITY definition."""
        self.match("KEYWORD", "ENTITY")
        self.match("IDENTIFIER")  # Entity name
        self.match("SEPARATOR", ":")
        self.attribute_list()

    def attribute_list(self):
        """Parses a list of attributes."""
        self.attribute()
        while self.current_token and self.current_token.type_ == "SEPARATOR" and self.current_token.value == ",":
            self.advance()  # Skip the comma
            self.attribute()

    def attribute(self):
        """Procesa un atributo dentro de una entidad."""
        self.match("IDENTIFIER")  # Nombre del atributo
        self.match("SEPARATOR", ":")  # Dos puntos (:)
        self.property_list()  # Procesamos la lista de propiedades

    def attribute_list(self):
        """Parses a list of attributes where each attribute ends with ';'."""
        while self.current_token and self.current_token.type_ == "IDENTIFIER":
            self.attribute()
            self.match("TERMINATOR")  # Cada atributo debe terminar con ';'

    def relationship(self):
        """Parses a RELATIONSHIP definition."""
        self.match("KEYWORD", "RELATIONSHIP")
        self.match("IDENTIFIER")  # Relationship name
        self.match("SEPARATOR", ":")
        self.match("IDENTIFIER")  # First entity
        self.match("KEYWORD", "GO")
        self.match("IDENTIFIER")  # Second entity
        self.match("SEPARATOR", ":")
        self.match("KEYWORD")  # Cardinality (ONE_TO_ONE, ONE_TO_MANY, MANY_TO_MANY)
        self.match("TERMINATOR")  # Relación debe terminar en ';'

    def property_list(self):
        """Procesa la lista de propiedades separadas por comas."""
        while self.current_token and self.current_token.type_ == "PROPERTY":
            self.match("PROPERTY")
            if self.current_token and self.current_token.type_ == "SEPARATOR" and self.current_token.value == ",":
                self.match("SEPARATOR")  # Consume la coma si hay más propiedades

    def match(self, expected_type, expected_value=None):
        """Checks if the current token matches the expected type and value."""
        if self.current_token is None:
            self.error(expected_value or expected_type)
        if self.current_token.type_ != expected_type:
            self.error(expected_type)
        if expected_value and self.current_token.value != expected_value:
            self.error(expected_value)
        self.advance()

    def error(self, expected):
        """Raises an exception when an unexpected token is encountered."""
        raise Exception(
            f"Syntax error: expected {expected}, found {self.current_token}"
        )
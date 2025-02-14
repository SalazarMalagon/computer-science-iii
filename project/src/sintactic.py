# <S>                       -> <ENTITY_DEFINITION> | <RELATIONSHIP_DEFINITION>

# <ENTITY_DEFINITION>       -> "ENTITY" <IDENTIFIER> ":" <ATTRIBUTE_LIST>

# <ATTRIBUTE_LIST>          -> <ATTRIBUTE> ";" | <ATTRIBUTE> ";" <ATTRIBUTE_LIST>
# <ATTRIBUTE>               -> <IDENTIFIER> ":" <ATTRIBUTE_PROPERTIES>
# <ATTRIBUTE_PROPERTIES>    -> <PROPERTY> | <PROPERTY> "," <ATTRIBUTE_PROPERTIES>
# <PROPERTY>                -> "PK" | "NON_PK" | "NON_NULL" | "NULL" | "INT" | "CHAR" | "AUT" | "NON_AUT"

# <RELATIONSHIP_DEFINITION> -> "RELATIONSHIP" <IDENTIFIER> ":" <RELATION_DETAILS>
# <RELATION_DETAILS>        -> <IDENTIFIER> "GO" <IDENTIFIER> ":" <CARDINALITY> ";"
# <CARDINALITY>             -> "ONE_TO_ONE" | "ONE_TO_MANY" | "MANY_TO_MANY"
class SintacticAnalyzer:
    """Syntactic parser for the entity and relationship definition language."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        """Move on to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def error(self, expected):
        line = self.current_token.line if self.current_token else "desconocida"
        column = self.current_token.column if self.current_token else "desconocida"
        raise SyntaxError(
            f"Syntactic error on line {line}, column {column}: "
            f"It was expected {expected}, but was found '{self.current_token.value}'"
        )

    def match(self, token_type, value=None):
        """Verify that the current token is of the expected type (and value) and move on."""
        if self.current_token is None:
            self.error(f"{token_type} {value if value else ''}")
        if self.current_token.type_ != token_type:
            self.error(token_type)
        if value is not None and self.current_token.value != value:
            self.error(f"{token_type} with value {value}")
        self.advance()

    def parse(self):
        """
        Main method of analysis.
        <S> -> <ENTITY_DEFINITION> | <RELATIONSHIP_DEFINITION>
        The code is expected to contain one or more definitions.
        """
        while self.current_token is not None:
            if self.current_token.type_ == "KEYWORD":
                if self.current_token.value == "ENTITY":
                    self.parse_entity_definition()
                elif self.current_token.value == "RELATIONSHIP":
                    self.parse_relationship_definition()
                else:
                    self.error("ENTITY o RELATIONSHIP")
            else:
                self.error("KEYWORD")
        print("Syntactic analysis completed successfully.")

    def parse_entity_definition(self):
        """
        <ENTITY_DEFINITION> -> "ENTITY" <IDENTIFIER> ":" <ATTRIBUTE_LIST>
        """
        self.match("KEYWORD", "ENTITY")
        self.match("IDENTIFIER")
        self.match("TERMINATOR", ":")
        self.parse_attribute_list()

    def parse_attribute_list(self):
        """
        <ATTRIBUTE_LIST> -> <ATTRIBUTE> ";" | <ATTRIBUTE> ";" <ATTRIBUTE_LIST>
        At least one attribute is processed, followed by ';'. If another identifier follows, the list is continued.
        """
        self.parse_attribute()
        self.match("SEMITERMINATOR", ";")
        # As long as the next token is an identifier, we assume there is another attribute
        while self.current_token is not None and self.current_token.type_ == "IDENTIFIER":
            self.parse_attribute()
            self.match("SEMITERMINATOR", ";")

    def parse_attribute(self):
        """
        <ATTRIBUTE> -> <IDENTIFIER> ":" <ATTRIBUTE_PROPERTIES>
        """
        self.match("IDENTIFIER")
        self.match("TERMINATOR", ":")
        self.parse_attribute_properties()

    def parse_attribute_properties(self):
        """
        <ATTRIBUTE_PROPERTIES> -> <PROPERTY> | <PROPERTY> "," <ATTRIBUTE_PROPERTIES>
        At least one property is processed. If there is a comma, more properties are expected.
        """
        properties = []

        properties.append(self.current_token.value)
        self.match("PROPERTY")
        while self.current_token is not None and self.current_token.type_ == "SEPARATOR":
            self.match("SEPARATOR", ",")
            properties.append(self.current_token.value)
            self.match("PROPERTY")

        if len(properties) != 4:
            line = self.current_token.line if self.current_token else "desconocida"
            column = self.current_token.column if self.current_token else "desconocida"
            raise SyntaxError(
                f"Syntactic error on line {line}, column {column}: "
                f"An attribute must have exactly 4 properties, but it has {len(properties)}."
            )

    def parse_relationship_definition(self):
        """
        <RELATIONSHIP_DEFINITION> -> "RELATIONSHIP" <IDENTIFIER> ":" <RELATION_DETAILS>
        """
        self.match("KEYWORD", "RELATIONSHIP")
        self.match("IDENTIFIER")
        self.match("TERMINATOR", ":")
        self.parse_relation_details()

    def parse_relation_details(self):
        """
        <RELATION_DETAILS> -> <IDENTIFIER> "GO" <IDENTIFIER> ":" <CARDINALITY> ";"
        """
        self.match("IDENTIFIER")
        self.match("KEYWORD", "GO")
        self.match("IDENTIFIER")
        self.match("TERMINATOR", ":")
        self.match("CARDINALITY")
        self.match("SEMITERMINATOR", ";")

    def __repr__(self):
        return f"SintacticAnalyzer(pos={self.pos}, current_token={self.current_token})"

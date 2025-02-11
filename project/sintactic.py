# <S>                       -> <ENTITY_DEFINITION> | <RELATIONSHIP_DEFINITION>

# <ENTITY_DEFINITION>       -> "ENTITY" <IDENTIFIER> ":" <ATTRIBUTE_LIST>

# <ATTRIBUTE_LIST>          -> <ATTRIBUTE> ";" | <ATTRIBUTE> ";" <ATTRIBUTE_LIST>
# <ATTRIBUTE>               -> <IDENTIFIER> ":" <ATTRIBUTE_PROPERTIES>
# <ATTRIBUTE_PROPERTIES>    -> <PROPERTY> | <PROPERTY> "," <ATTRIBUTE_PROPERTIES>
# <PROPERTY>                -> "PK" | "NON_PK" | "NON_NULL" | "NULL" | "INT" | "CHAR" | "AUT" | "NON_AUT"

# <RELATIONSHIP_DEFINITION> -> "RELATIONSHIP" <IDENTIFIER> ":" <RELATION_DETAILS>
# <RELATION_DETAILS>        -> <IDENTIFIER> "GO" <IDENTIFIER> ":" <CARDINALITY>
# <CARDINALITY>             -> "ONE_TO_ONE" | "ONE_TO_MANY" | "MANY_TO_MANY"
class SintacticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        if self.current_token and self.current_token.type_ == 'KEYWORD':
            if self.current_token.value == 'ENTITY':
                self.entity_definition()
            elif self.current_token.value == 'RELATIONSHIP':
                self.relationship_definition()
            else:
                self.error('ENTITY or RELATIONSHIP')
        else:
            self.error('KEYWORD')

    def entity_definition(self):
        self.match('KEYWORD', 'ENTITY')
        self.match('IDENTIFIER')
        self.match('TERMINATOR', ':')
        self.attribute_list()

    def attribute_list(self):
        self.attribute()
        while self.current_token and self.current_token.type_ == 'SEMITERMINATOR':
            self.advance()
            if self.current_token and self.current_token.type_ == 'IDENTIFIER':
                self.attribute()

    def attribute(self):
        self.match('IDENTIFIER')
        self.match('TERMINATOR', ':')
        self.attribute_properties()

    def attribute_properties(self):
        self.match('PROPERTY')
        while self.current_token and self.current_token.type_ == 'SEPARATOR':
            self.advance()
            self.match('PROPERTY')

    def relationship_definition(self):
        self.match('KEYWORD', 'RELATIONSHIP')
        self.match('IDENTIFIER')
        self.match('TERMINATOR', ':')
        self.relation_details()

    def relation_details(self):
        self.match('IDENTIFIER')
        self.match('KEYWORD', 'GO')
        self.match('IDENTIFIER')
        self.match('TERMINATOR', ':')
        self.match('CARDINALITY')

    def match(self, expected_type, expected_value=None):
        if self.current_token and self.current_token.type_ == expected_type:
            if expected_value and self.current_token.value != expected_value:
                self.error(expected_value)
            self.advance()
        else:
            self.error(expected_type)

    def error(self, expected):
        raise Exception(f"Syntax error: expected {expected}, found {self.current_token}")

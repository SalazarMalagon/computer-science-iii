"""This script demonstrates how to use the compiler with an entity-relationship model."""

from compiler import Compiler

if __name__ == "__main__":
    """Main execution block that defines an entity-relationship model and compiles it."""
    
    # Define an entity-relationship model as input
    code = """
    ENTITY autor :
        id: PK, NON_NULL, INT, NON_AUT;
        nombre: NON_PK, NON_NULL, CHAR, NON_AUT;

    ENTITY libro :
        codigo: PK, NON_NULL, INT, AUT;
        autor: NON_PK, NON_NULL, CHAR, NON_AUT;
    
    RELATIONSHIP escribir :
        autor GO libro : ONE_TO_MANY;

    """
    
    # Initialize the compiler instance
    compiler = Compiler()
    
    # Compile the entity-relationship model into an SQL script
    compiler.compile(code, "mi_base_de_datos.sql")
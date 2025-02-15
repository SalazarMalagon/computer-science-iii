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

    code2 = """
    ENTITY estudiante :
        id: PK, NON_NULL, INT, AUT;
        nombre: NON_PK, NON_NULL, CHAR, NON_AUT;
        edad: NON_PK, NON_NULL, INT, NON_AUT;

    ENTITY curso :
        codigo: PK, NON_NULL, INT, NON_AUT;
        titulo: NON_PK, NON_NULL, CHAR, NON_AUT;

    RELATIONSHIP inscripcion :
        estudiante GO curso : ONE_TO_ONE;
    """

    code3 = """
    ENTITY cliente :
        id: PK, NON_NULL, INT, AUT;
        nombre: NON_PK, NON_NULL, CHAR, NON_AUT;
        email: NON_PK, NON_NULL, CHAR, NON_AUT;

    ENTITY pedido :
        numero: PK, NON_NULL, INT, AUT;
        fecha: NON_PK, NON_NULL, CHAR, NON_AUT;
        total: NON_PK, NON_NULL, INT, NON_AUT;

    RELATIONSHIP realizar :
        cliente GO pedido : ONE_TO_MANY;
    """
    
    # Initialize the compiler instance
    compiler = Compiler()
    
    # Compile the entity-relationship model into an SQL script
    compiler.compile(code2, "mi_base_de_datos.sql")
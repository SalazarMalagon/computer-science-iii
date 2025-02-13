from compiler import Compiler

if __name__ == "__main__":
    code = """
ENTITY libro :
    codigo: PK, NON_NULL, INT, AUT;
    autor: NON_PK, NON_NULL, CHAR, NON_AUT;

ENTITY autor :
    id: PK, NON_NULL, INT, NON_AUT;
    nombre: NON_PK, NON_NULL, CHAR, NON_AUT;

RELATIONSHIP escribir :
    autor GO libro : ONE_TO_MANY;
    """
    
    compiler = Compiler()
    compiler.compile(code, "mi_base_de_datos.sql")
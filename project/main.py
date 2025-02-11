from Lexcal import checker
from sintactic import SintacticAnalyzer
#from semantic import SemanticAnalyzer

if __name__ == '__main__':
    code = """

ENTITY libro :
    codigo: PK, NON_NULL, INT, AUT;
    autor: NON_PK, NON_NULL, CHAR, NON_AUT;


RELATIONSHIP escribir :
    autor GO libro : ONE_TO_MANY;

"""
    new_code = checker(code)
    print(new_code)
    sintactic_analyzer = SintacticAnalyzer(new_code)
    sintactic_analyzer.parse()
    print(sintactic_analyzer)
    #semantic_analyzer = SemanticAnalyzer(new_code)
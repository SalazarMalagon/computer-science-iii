import os

from Lexcal import checker
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

class Compiler:
    def compile(self, code: str, output_file: str = "database.sql"):
        # Análisis léxico
        tokens = checker(code)
        print(tokens)
        
        # Análisis sintáctico
        sintactic_analyzer = SintacticAnalyzer(tokens)
        sintactic_analyzer.parse()
        print(sintactic_analyzer)
        
        # Análisis semántico
        semantic_analyzer = SemanticAnalyzer(tokens)
        semantic_structure = semantic_analyzer.analyze()
        
        if semantic_structure:
            print("Errores semánticos:")
            for error in semantic_structure:
                print(f"- {error}")
            return
        else:
            print("\nAnálisis semántico exitoso!")


        # Generación de código SQL
        # code_gen = CodeGenerator()
        # sql_code = code_gen.generate_sql(semantic_structure)
        
        # # Guardar en archivo
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # project_root = os.path.dirname(current_dir)
        # sql_folder = os.path.join(project_root, "SQL")
        # output_file = os.path.join(sql_folder, "output.sql")
        # with open(output_file, "w", encoding="utf-8") as f:
        #     f.write(sql_code)

        # print(f"Archivo guardado en: {output_file}")

        
import os
import shutil

from Lexcal import checker
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from diaggen import diaggen

class Compiler:
    """Compiler class that processes entity-relationship models."""
    
    def compile(self, code: str, output_file: str = "database.sql"):
        """Compiles the input entity-relationship model into SQL and generates a diagram."""
        
        # Lexical analysis
        tokens = checker(code)
        print(tokens)
        
        # Syntactic analysis
        sintactic_analyzer = SintacticAnalyzer(tokens)
        sintactic_analyzer.parse()
        print(sintactic_analyzer)
        
        # Semantic analysis
        semantic_analyzer = SemanticAnalyzer(tokens)
        semantic_errors = semantic_analyzer.analyze()
        
        if semantic_errors:
            print("Semantic errors:")
            for error in semantic_errors:
                print(f"- {error}")
            return
        else:
            print("\nSemantic analysis successful!")
            semantic_data = {
                'entities': semantic_analyzer.entities,
                'relationships': semantic_analyzer.relationships
            }

        # SQL code generation
        code_gen = CodeGenerator()
        sql_code = code_gen.generate_sql(semantic_data)
        
        # Save to file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        sql_folder = os.path.join(project_root, "SQL")

        # Clean existing SQL folder
        if os.path.exists(sql_folder):
            for file in os.listdir(sql_folder):
                file_path = os.path.join(sql_folder, file)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) 
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  
        
        # Save the new SQL file
        output_file = os.path.join(sql_folder, "output.sql")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sql_code)
        
        print(f"File saved in: {output_file}")
        
        # Parse and generate diagram
        tables = diaggen.parse_sql_file(output_file)
        diaggen.graficar_diagrama(tables, zoom_factor=0.8)

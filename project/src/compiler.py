import os
import shutil
import tkinter as tk
from tkinter import ttk


from Lexcal import checker
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from diaggen import diaggen

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
        semantic_errors = semantic_analyzer.analyze()
        
        if semantic_errors:
            print("Errores semánticos:")
            for error in semantic_errors:
                print(f"- {error}")
            return
        else:
            print("\nAnálisis semántico exitoso!")
            semantic_data = {
                'entities': semantic_analyzer.entities,
                'relationships': semantic_analyzer.relationships
            }
    # Generación de código SQL

        # Generación de código SQL
        code_gen = CodeGenerator()
        sql_code = code_gen.generate_sql(semantic_data)
        
        # Guardar en archivo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        sql_folder = os.path.join(project_root, "SQL")

        if os.path.exists(sql_folder):
                    for file in os.listdir(sql_folder):
                        file_path = os.path.join(sql_folder, file)
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path) 
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)  
                
        # Guardar el nuevo archivo SQL
        output_file = os.path.join(sql_folder, "output.sql")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sql_code)

        print(f"Archivo guardado en: {output_file}")


        # Parsear y generar diagrama

        """Función principal que inicializa Tkinter y muestra el gráfico."""
        """root = tk.Tk()
        root.title("Diagrama Relacional")

        ttk.Label(root, text="Diagrama Relacional Generado", font=("Arial", 14)).pack(pady=10)

        tables = diaggen.parse_sql_file(output_file)
        G = diaggen.draw_schema(tables)

        diaggen.plot_graph(G, root)

        root.mainloop()"""

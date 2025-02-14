# Proyecto: Compilador Simple

Este proyecto es un compilador simple que sigue el flujo tradicional de compilación: análisis léxico, análisis sintáctico, análisis semántico y generación de código.

## Estructura del Proyecto

- `requirements.txt` → Lista de dependencias necesarias.
- `SQL/output.sql` → Archivo SQL generado por el compilador.
- `src/` → Código fuente del compilador:
  - `codegen.py` → Generador de código SQL.
  - `compiler.py` → Módulo principal del compilador.
  - `diaggen.py` → Generador de diagramas E-R.
  - `Lexcal.py` → Análisis léxico.
  - `sintactic.py` → Análisis sintáctico.
  - `semantic.py` → Análisis semántico.
  - `main.py` → Punto de entrada del programa.

## Cómo Funciona

El compilador sigue las siguientes fases:
1. **Análisis Léxico** → Identifica los tokens en el código de entrada.
2. **Análisis Sintáctico** → Verifica la estructura del código según la gramática definida.
3. **Análisis Semántico** → Asegura que las reglas semánticas sean correctas.
4. **Generación de Código** → Traduce el código a SQL y genera un diagrama E-R.

## Diagrama Generativo

```plaintext
<S>                       -> <ENTITY_DEFINITION> | <RELATIONSHIP_DEFINITION>
<ENTITY_DEFINITION>       -> "ENTITY" <IDENTIFIER> ":" <ATTRIBUTE_LIST>
<ATTRIBUTE_LIST>          -> <ATTRIBUTE> ";" | <ATTRIBUTE> ";" <ATTRIBUTE_LIST>
<ATTRIBUTE>               -> <IDENTIFIER> ":" <ATTRIBUTE_PROPERTIES>
<ATTRIBUTE_PROPERTIES>    -> <PROPERTY> | <PROPERTY> "," <ATTRIBUTE_PROPERTIES>
<PROPERTY>                -> "PK" | "NON_PK" | "NON_NULL" | "NULL" | "INT" | "CHAR" | "AUT" | "NON_AUT"
<RELATIONSHIP_DEFINITION> -> "RELATIONSHIP" <IDENTIFIER> ":" <RELATION_DETAILS>
<RELATION_DETAILS>        -> <IDENTIFIER> "GO" <IDENTIFIER> ":" <CARDINALITY> ";"
<CARDINALITY>             -> "ONE_TO_ONE" | "ONE_TO_MANY" | "MANY_TO_MANY"
```

### Ejemplo de Entrada

```plaintext
ENTITY libro :
    codigo: PK, NON_NULL, INT, AUT;
    autor: NON_PK, NON_NULL, CHAR, NON_AUT;

ENTITY autor :
    id: PK, NON_NULL, INT, NON_AUT;
    nombre: NON_PK, NON_NULL, CHAR, NON_AUT;

RELATIONSHIP escribir :
    autor GO libro : ONE_TO_MANY;
```

### Salida Generada

1. **Archivo SQL**: Se genera un archivo `output.sql` con la estructura de la base de datos.
2. **Diagrama E-R**: Se genera un representación gráfica (simple) con matplotlib y networkx de la base de datos.

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/SalazarMalagon/computer-science-iii.git
   cd project
   ```
2. Crear y activar un entorno virtual (opcional pero recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate     # En Windows
   ```
3. Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

en el archivo **main.py**, en la variable **code**, debes escribir tu base de datos a crear siguiendo las reglas propuestas por el proyecto, como lo expuesto en el diagrama generativo y teneiendo en cuenta el siguiente listado de tokens:

  ```plaintext
  TOKEN_TYPES = [
      ('KEYWORD', r'\b(ENTITY|RELATIONSHIP|GO)\b'),
      ('CARDINALITY', r'\b(ONE_TO_ONE|ONE_TO_MANY|MANY_TO_MANY)\b'),
      ('PROPERTY', r'\b(PK|NON_PK|NON_NULL|NULL|INT|CHAR|AUT|NON_AUT)\b'),
      ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
      ('TERMINATOR', r':'),
      ('SEPARATOR', r','),
      ('SEMITERMINATOR', r';'),
      ('COMMENT', r'//.*'),
      ('WHITESPACE', r'[ \t]+'),
      ('NEWLINE', r'\n'),
      ('MISMATCH', r'.')
  ]
  ```

Para ejecutar el compilador:
  ```sh
  python src/main.py
  ```

## Requisitos

El compilador genera una imagen y un archivo SQL como salida utilizando **so,  matplotlib y networkx**, por lo que debes asegurarte de que esté instalado en tu sistema:

  ```sh
  pip install so matplotlib networkx
  ```
O puedes ejecutar:

   Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```

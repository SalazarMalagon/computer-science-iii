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

```
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

```
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
2. **Diagrama E-R**: Se genera una representación gráfica (simple) de la base de datos con matplotlib y networkx.

## Instalación

### Clonar el repositorio
```sh
 git clone https://github.com/SalazarMalagon/computer-science-iii.git
 cd project
```

### Crear y activar un entorno virtual (opcional pero recomendado)
```sh
# En Linux/macOS
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### Instalar dependencias
```sh
pip install -r requirements.txt
```

## Uso

En el archivo **main.py**, en la variable **code**, debes escribir la base de datos que deseas crear siguiendo las reglas del diagrama generativo.

### Tokens Reconocidos

El compilador reconoce los siguientes tipos de tokens:
- **Palabras clave**: ENTITY, RELATIONSHIP, GO.
- **Cardinalidades**: ONE_TO_ONE, ONE_TO_MANY, MANY_TO_MANY.
- **Propiedades de los atributos**(se deben poner las 4 propiedades sin ser contradictorios, no puede se PK y NON_PK al tiempo): PK, NON_PK, NON_NULL, NULL, INT, CHAR, AUT, NON_AUT.
- **Identificadores**: Nombres de entidades, relaciones y atributos.
- **Símbolos especiales**: Dos puntos `:` para definir atributos, punto y coma `;` como terminador, coma `,` para separar propiedades.
- **Comentarios**: Se permiten comentarios con `//`.

#### Ejemplo de Reconocimiento de Tokens
Para la siguiente línea de código:
```
codigo: PK, NON_NULL, INT, AUT;
```
El analizador léxico generará:
```
IDENTIFIER: codigo
TERMINATOR: :
PROPERTY: PK
SEPARATOR: ,
PROPERTY: NON_NULL
SEPARATOR: ,
PROPERTY: INT
SEPARATOR: ,
PROPERTY: AUT
SEMITERMINATOR: ;
```

### Ejecutar el Compilador
```sh
python src/main.py
```

## Requisitos

El compilador genera una imagen y un archivo SQL como salida utilizando **matplotlib y networkx**, por lo que debes asegurarte de que estén instalados en tu sistema:
```sh
pip install matplotlib networkx
```
O instalar todas las dependencias de una vez con:
```sh
pip install -r requirements.txt
```


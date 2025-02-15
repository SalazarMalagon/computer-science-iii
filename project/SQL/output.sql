CREATE TABLE estudiante (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    edad INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE curso (
    codigo INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    PRIMARY KEY (codigo)
);

ALTER TABLE curso ADD COLUMN estudiante_id INT UNIQUE;

ALTER TABLE curso ADD FOREIGN KEY (estudiante_id) REFERENCES estudiante(id);
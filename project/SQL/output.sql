CREATE TABLE libro (
    codigo INT NOT NULL AUTO_INCREMENT,
    autor VARCHAR(255) NOT NULL,
    PRIMARY KEY (codigo)
);

CREATE TABLE autor (
    id INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE libro ADD COLUMN autor_id INT;

ALTER TABLE libro ADD FOREIGN KEY (autor_id) REFERENCES autor(id);
CREATE TABLE libro (
    codigo INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (codigo)
);

CREATE TABLE autor (
    id INT NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE libro ADD COLUMN autor_id INT;

ALTER TABLE libro ADD FOREIGN KEY (autor_id) REFERENCES autor(id);
CREATE TABLE usuario (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE perfil (
    id INT NOT NULL AUTO_INCREMENT,
    descripcion VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE publicacion (
    id INT NOT NULL AUTO_INCREMENT,
    contenido VARCHAR(255) NOT NULL,
    fecha VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE comentario (
    id INT NOT NULL AUTO_INCREMENT,
    texto VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE reaccion (
    id INT NOT NULL AUTO_INCREMENT,
    tipo VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE perfil ADD COLUMN usuario_id INT UNIQUE;

ALTER TABLE perfil ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id);

ALTER TABLE publicacion ADD COLUMN usuario_id INT;

ALTER TABLE publicacion ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id);

ALTER TABLE comentario ADD COLUMN usuario_id INT;

ALTER TABLE comentario ADD FOREIGN KEY (usuario_id) REFERENCES usuario(id);

CREATE TABLE usuario_reaccion (

    usuario_id INT NOT NULL,

    reaccion_id INT NOT NULL,

    PRIMARY KEY (usuario_id, reaccion_id),

    FOREIGN KEY (usuario_id) REFERENCES usuario(id),

    FOREIGN KEY (reaccion_id) REFERENCES reaccion(id)

);

ALTER TABLE comentario ADD COLUMN publicacion_id INT;

ALTER TABLE comentario ADD FOREIGN KEY (publicacion_id) REFERENCES publicacion(id);

ALTER TABLE reaccion ADD COLUMN publicacion_id INT;

ALTER TABLE reaccion ADD FOREIGN KEY (publicacion_id) REFERENCES publicacion(id);
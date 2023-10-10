INSERT INTO roles VALUES (1, 'ADMINISTRADOR', 1);
INSERT INTO roles VALUES (2, 'PROPIETARIO', 1);
INSERT INTO roles VALUES (3, 'CLIENTE', 1);

INSERT INTO type_field_soccer VALUES (1, 'SINTÉTICO', 1);
INSERT INTO type_field_soccer VALUES (2, 'LOZA', 1);

INSERT INTO users(id, first_name, last_name, phone, email, password, status, created_at,
updated_at, rol_id)
VALUES(1, 'LUIS FELIPE', 'HUARANCA BERROSPI', '967807471', 'luis.fhb.2016@gmail.com',
'pbkdf2_sha256$390000$PChAgyU2xuztZxUb0SPylU$oI7rwsLa2NFBOgjl460DZRhpPVQRJmf9qDC6xkTatjM=', 1, '2023-04-16', '2023-04-16', 1);

INSERT INTO users(id, first_name, last_name, phone, email, password, status, created_at,
updated_at, rol_id)
VALUES(2, 'PROPIETARIO', 'PROPIETARIO', '967807471', 'propietario@gmail.com',
'pbkdf2_sha256$390000$PChAgyU2xuztZxUb0SPylU$oI7rwsLa2NFBOgjl460DZRhpPVQRJmf9qDC6xkTatjM=', 1, '2023-04-16', '2023-04-16', 1);

INSERT INTO users(id, first_name, last_name, phone, email, password, status, created_at,
updated_at, rol_id)
VALUES(3, 'CLIENTE', 'CLIENTE', '967807471', 'cliente@gmail.com',
'pbkdf2_sha256$390000$PChAgyU2xuztZxUb0SPylU$oI7rwsLa2NFBOgjl460DZRhpPVQRJmf9qDC6xkTatjM=', 1, '2023-04-16', '2023-04-16', 1);
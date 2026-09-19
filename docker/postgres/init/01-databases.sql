CREATE DATABASE lab4;
CREATE DATABASE lab5;
CREATE DATABASE mikedb;
CREATE DATABASE admin_bank;
CREATE DATABASE practica1;

CREATE USER mike WITH PASSWORD 'super_secret_password';
ALTER DATABASE mikedb OWNER TO mike;
ALTER DATABASE lab4 OWNER TO mike;

CREATE USER user_admin_bank WITH PASSWORD 'pass_admin_bank';
ALTER DATABASE admin_bank OWNER TO user_admin_bank;

GRANT ALL PRIVILEGES ON DATABASE lab5 TO universidad;
GRANT ALL PRIVILEGES ON DATABASE universidad TO universidad;
GRANT ALL PRIVILEGES ON DATABASE practica1 TO universidad;

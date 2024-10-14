-- create the user
CREATE USER "YourShopDB_Admin" WITH PASSWORD 'YourShopDB_Admin_pwd';

-- create the database
CREATE DATABASE "YourShopDB";

-- connect to the YourShopDB database as a superuser (e.g., postgres)
\c "YourShopDB"

-- grant all privileges on the database to YourShopDB_Admin
GRANT ALL PRIVILEGES ON DATABASE "YourShopDB" TO "YourShopDB_Admin";

-- grant usage and create privileges on the public schema
GRANT USAGE, CREATE ON SCHEMA public TO "YourShopDB_Admin";

-- grant all privileges on all tables in the public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "YourShopDB_Admin";

-- grant all privileges on all sequences in the public schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "YourShopDB_Admin";

-- make YourShopDB_Admin the owner of the public schema
ALTER SCHEMA public OWNER TO "YourShopDB_Admin";

-- make future tables to be owned by YourShopDB_Admin by default:
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO "YourShopDB_Admin";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO "YourShopDB_Admin";
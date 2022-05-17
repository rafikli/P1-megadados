# P1-megadados

Para criar a base basta rodar o script create_db.sql no MySQL

Defina a senha e usuario do MySQL em um arquivo .env:

USER = "usuario"
PASSWORD = "senha"

Rode o programa com:

$ uvicorn sql_app.main:app --reload
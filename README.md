# Venda Fácil - Univesp

## Requerimentos

Criar o arquivo .env na raiz do projeto e preencher a variável DATABASE_URL.

A usada no meu computador localmente: 
```
DATABASE_URL=postgresql+psycopg2://postgres:delta@localhost:5432/venda_facil
```

## Nova Estrutura
```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

set FLASK_ENV=development

alembic upgrade head

flask run
```

### Estrutura Anterior
```bash
py -3 -m venv .venv

.venv/Scripts/activate

pip install Flask flask_sqlalchemy
```
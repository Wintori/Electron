# Electron

# Create database:
```docker run  --name PID-database -e POSTGRES_USER=postres -e POSTGRES_DB=PIDdatabase -e POSTGRES_PASSWORD=postres -e PGDATA=/var/lib/postgresql/data/pgdata -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres```
or  
```docker-compose -f docker-compose.yml up```
# Install requirement
```poetry install```
 if error `pip install poetry`


if it is hard:
``pip install -r res.txt ``

# Миграции отсуствуют временно
(при 1 запуске база автоматически создает таблицы ) 

# Запуск сервера: 
`python3 back/main.py`

# Open API 3 :
```API_Doc.yaml```
# Кейс от Fast Reports

![FastReports](https://www.softmagazin.ru/upload/iblock/d44/d44273acbee5401798ac42191653b515.png)


# Ссылка на сборку 
[Google Drive](https://clck.ru/32jBWR)
  

# Figma проекта
[Figma](https://www.figma.com/file/JmZPCh45jgzhmI2qvYzoFY/Untitled?t=jNm6G5Kg8qUzZGis-1)
  
# Установка при запуске через клонирование

## Create database:
```docker run  --name PID-database -e POSTGRES_USER=postres -e POSTGRES_DB=PIDdatabase -e POSTGRES_PASSWORD=postres -e PGDATA=/var/lib/postgresql/data/pgdata -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres```
<br/>or
<br/>
```docker-compose -f docker-compose.yml up```
## Install requirement
```poetry install```
 if error `pip install poetry`
 
 if have trubles with it:
 
 `pip install -r req.txt`
 

## Миграции отсуствуют временно
(при 1 запуске база автоматически создает таблицы ) 
# Запуск фронтенда 
`npm install
npm start`
## Запуск сервера: 
`python3 back/main.py`

## Open API 3 :
```API_Doc.yaml```

# Что там с фронтом?
<br/>
* Методология БЭМ
* Семантическая вёрстка
* Работа на чисто JS
* Адаптивная верстка (в разработке)

---

Вы можете посмотреть как работает наш API онлайн, поместив файл [API_Doc.yaml](https://drive.google.com/file/d/1L81MZfjckXV2efivKMs1ECeg86aN0htw/view?usp=share_link) на сайт [Swagger](https://editor.swagger.io/).

---
# Команда разработчиков

* **Перевощиков Андрей** / Backend разработчик / [GitHub](https://github.com/andreyvaran)
* **Шашурин Егор** / Frontend разработчик / [GitHub](https://github.com/Wintori)
* **Плехов Андрей** / Frontend разработчик / [GitHub](https://github.com/fundxx)

# user_response_app


## Что делает проект

Проект преставляет собой backend часть, который осуществляет ответы на запрос от другого приложения (чтобы клонировать приложение user_request_app
)

```Bash 
git clone https://github.com/aidarhaertdinov/user_request_app.git
```
Реализована базовая и токеновая аутентификация.

## Как собрать и запустить проект

### Для Windows:

1. Клонировать проект выполнив команду
```Bash 
git clone https://github.com/aidarhaertdinov/user_response_app.git
```
2. Создать виртуальное окружение выполнив команду 
```Bash
python -m venv venv
``` 
3. Активировать виртуальное окружение выполнив команду
```Bash
venv\Scripts\activate
```  
4. Установить пакеты выполнив команду 
```Bash
pip freeze > requirements.txt
```
5. Установить миграцию выполнив команду 
```Bash
pip install flask-migrate
``` 
6. Создать репозиторий миграции выполнив команду 
```Bash
flask db init
``` 

## Используемые Конфигураций (Config)


```Python
SECRET_KEY = os.urandom(32)
```
- используют значение секретного ключа в качестве криптографического ключа, полезного для генерации подписей или токенов. [ссылка на документацию](https://explore-flask.readthedocs.io/en/latest/configuration.html)


```Python
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
- если установлен  `True`, то Flask-SQLAlchemy будет отслеживать изменения объектов и посылать сигналы. [ссылка на документацию](https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html)






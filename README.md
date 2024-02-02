**Дипломный проект «Платформа для публикаций платного контента»**

Цель проекта:
Создание веб-приложения, на котором пользователь может размещать бесплатный и платный контент по подписке. Платный контент могут видеть только авторизованные подписчики сервиса. Бесплатный контент же находится в открытом доступе для неавторизованных пользователей без подписки.

Создайте виртуальное окружение poetry командой:

    poetry init

Установите зависимости командой:
   
    poetry install

Создайте миграции командами:
python manage.py makemigrations

    python manage.py migrate

Создайте Базу Данных (в данном проекте используется PostgreSQL).

Перейдите в файл '.env.sample'. Заполните в этом файле все необходимые поля, создайте в директории проекта файл '.env' и перенесите туда заполненный в '.env.sample' шаблон.

Ниже приведен пример заполнения:



    SECRET_KEY_DJANGO='your_personal_secret_key'
    POSTGRES_USER='postgres_user'
    POSTGRES_PASSWORD='postgres_password'
    POSTGRES_DB='database_name'
    POSTGRES_HOST='postgres_host'
    PG_DATA=/path
    LOCATION='redis://host:port'
    CACHE_ENABLED='True'
    STRIPE_API_KEY='stripe_api_key'
    YOUR_DOMAIN="http://host"
    TIME_ZONE='Zone/CityCenter'


Для демонстрации работы модели платной подписки используется сервис Stripe.

Получить API KEY можно на сайте с документацией https://stripe.com/docs/keys

Команда для создания админа [createadmin](/users/management/commands/createadmin.py) (Номер телефона '1234', Пароль 'admin'):

    python3 manage.py createadmin

Команда для заполнения базы данных для демонстрации [fill](/content_app/management/commands/fill.py):

    python3 manage.py fill

Завершение работы
Для остановки работы сервера используйте комбинацию клавиш Ctrl+C в окне терминала, где он был запущен.

Для остановки работы сервера Redis используйте команду: sudo service redis-server stop 

ПОКРЫТИЕ ТЕСТАМИ 78%

Запуск тестирования через консоль:

    python3 manage.py coverage users content_app

Проверка покрытия тестами:

    coverage report

🐋 Docker: запуск
Для запуска контейнеров в фоновом режиме выполните команду:

    docker-compose up -d --build

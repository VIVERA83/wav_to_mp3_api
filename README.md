# Wav to mp3 API

___

<span id="0"></span>

### <span id="1">1. </span><span style="color:purple">Описание</span>

Api сервис по хранеию звуковых файлов в формате mp3. Сервис позволяет пользователю сохранять звуковые файлы в формате
wav и скачивать их по ссылкам. Скачанный фаил будет иметь формат mp3. 
Документаци api сервису можно посмотреть по ссылке формата: http://{host}:{port}/docs
При запуске локально, можно попробовать перейти по ссылке http://0.0.0.0:8000/docs либо http://127.0.0.1:8000/docs
Точная ссылка к документации выводится в логах при запуске сервиса.

```
victorina    | 2023-01-01 00:00:00.000 | INFO     | core.app:setup_app:20 - Swagger link: http://0.0.0.0:8000/docs
```

___

### <span id="2">2. </span><span style="color:purple">Запуск серввиса через Docker-compose</span>

* </span><span style="color:orange">__Клонируем репозиторий:__</span>

```bash
git clone https://github.com/VIVERA83/wav_to_mp3_api.git
```

* </span><span style="color:orange">__Переходи в папку с проектом:__</span>

```bash
cd wav_to_mp3_api
```

* </span><span style="color:orange">__Создаем файл .env (с переменными окружения) на основе
  примера [.env_example](.env_example):__</span>

```bash
echo "# Настройка приложения
#LOGGING__LEVEL=INFO # Уровень логирования один из: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING__GURU=True # Алтернативный логер
LOGGING__TRACEBACK=True 

HOST=0.0.0.0
PORT=8000

POSTGRES__DB=test_db
POSTGRES__USER=test_user
POSTGRES__PASSWORD=pass
POSTGRES__HOST=postgres  #хост берется как имя сервиса в docker-compose.
POSTGRES__PORT=5432
POSTGRES__DB_SCHEMA=wav_to_mp3_api

# Настройка Postgres
POSTGRES_DB=test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=pass

# Настройка Uvicorn
UVICORN_WORKERS=3" >>.env
```

* </span><span style="color:orange">__Поднимаем Docker_compose контейнер:__</span>

```bash
docker-compose up --build
```

### <span id="3">3. </span><span style="color:purple">Примеры обращения к сервису</span>

* </span><span style="color:orange">__Документация:__</span>
  Поосле запуска сервиса, стновится доступна OpenAPi документация. Посмотреть ее можно по ссылке которая выводится в
  логах.
  Если сервис запускается локоально из под операционная системы Windows, то попробуйте перейти по следущей ссылке:
  http://127.0.0.1:8000/docs





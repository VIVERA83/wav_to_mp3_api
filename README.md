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
  примера [.env_example](.env_example)*:__</span>

```bash
echo "# Настройка приложения
#LOGGING__LEVEL=INFO # Уровень логирования один из: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING__GURU=True # Алтернативный логер
LOGGING__TRACEBACK=True 

HOST=0.0.0.0
PORT=8000

SIZE_WAV_FILE=1048576 # 1 Mb
SECRET_KEY=hello world

POSTGRES__DB=test_db
POSTGRES__USER=test_user
POSTGRES__PASSWORD=pass
POSTGRES__HOST=postgres_wav_to_mp3  #хост берется как имя сервиса в docker-compose.
POSTGRES__PORT=5432
POSTGRES__DB_SCHEMA=wav_to_mp3_api

# Настройка Postgres
POSTGRES_DB=test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=pass

# Настройка Uvicorn
UVICORN_WORKERS=3" >>.env
```

В ОС windows можно скопировать фаил [.env_example](.env_example) в `.env` командой, это будет равнозначно команде выше

```shell
copy /Y ".env_example" ".env"
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
* </span><span style="color:orange">__Скачать звуковой файил:__</span> будет совершина попытка скачать звуковой фаил
  
  http://127.0.0.1:8000/record?id=a17b2315-5bb8-40d3-8d8a-2d48b6c3144e&user=a17b2315-5bb8-40d3-8d8a-2d48b6c3144e
  * id файла `17b2315-5bb8-40d3-8d8a-2d48b6c3144e`
  * user_id пользователя `a17b2315-5bb8-40d3-8d8a-2d48b6c3144e`
  
  При наличии данного файла и пользователя будет получен запрос на загрузку файла.
  В случаии не удачи будет получен ответ вроде такого:
```json
{
    "detail": "Audio recording not found: id=d21b86da-e65f-47bb-8642-17cbe1e2bfdf user_id=6cfdd9b2-c7db-42ab-9156-75d86d4be110 .",
    "message": "See the documentation: http://0.0.0.0:8000/docs"
}
```


### <span id="4">4. </span><span style="color:purple">Для пользователей ОС Windows</span>

* доспуп к документации осуществляется по ссылкам
    * http://127.0.0.1:8000/docs
    * http://127.0.0.1:8000/redoc
    * http://localhost:8000/docs
    * http://localhost:8000/redoc

Для обращения к адресам 0.0.0.0 в брацзере можно установить плагин
[Redirector](https://chrome.google.com/webstore/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd/related)
после установки в плагине создать новый redirect со следующими настройками:

Description:

```commandline
0.0.0.0 to localhost
```

Include pattern:

```commandline
([a-zA-Z]*)://0.0.0.0:(\d*)/(.*)
```

Redirect to:

```commandline
$1://localhost:$2/$3
```

Pattern type: Regular Expression

![redirect.jpg](doc%2Fredirect.jpg)

После появится возможность открывать 0.0.0.0   

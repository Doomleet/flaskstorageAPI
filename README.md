## FlaskAPI


.env в /app
```
DB_USERNAME='postgres'
DB_PASSWORD='qasaq123'
DB_NAME='store'
DB_PORT='postgres'
```

.env рядом с docker-compose.yml
```
DB_NAME='store'
DB_USERNAME='postgres'
DB_PASSWORD='qasaq123'
```
Создание тестового пользователя:
```
docker compose -f docker-compose.yml up --build
docker compose -f docker-compose.yml exec api python3 -m utils.create_test_user
```


## Загрузка файла
### POST /upload

Загружает файл на сервер.

### Тело запроса

file: Файл для загрузки.

### Ответы

200 OK:
```
{
  "file_hash": "<file_hash>"
}
```

400 Неверный запрос:
```
{
  "error": "Файл не загружен"
}
```
или 
```
{
  "error": "Файл не добавлен"
}
```

## Скачивание файла
### GET /download/<file_hash>

Скачивает файл с сервера.

### Параметры пути

file_hash (строка): Хэш файла для скачивания.

### Ответы

200 OK: Скачивание файла.

404 Файл не найден:
```
{
  "error": "Файл не найден"
}
```

## Удаление файла
### DELETE /delete/<file_hash>

Удаляет файл с сервера.

### Параметры пути

file_hash (строка): Хэш файла для удаления.

### Ответы

200 OK:
```
{
  "message": "Файл удален"
}
```

404 Файл не найден:
```
{
  "error": "Файл не найден"
}
```
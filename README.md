
# Yandex.Disk File Manager

Веб-приложение для просмотра и скачивания файлов с публичных ссылок Яндекс.Диска.

## Функциональность

- Просмотр файлов по публичной ссылке Яндекс.Диска
- Фильтрация файлов по типу (документы, изображения)
- Скачивание отдельных файлов
- Пакетное скачивание нескольких файлов в ZIP-архиве

## Требования

- Python 3.8+
- Flask
- requests
- python-dotenv

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd yandex-disk-manager
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/MacOS
.venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта:
```
YANDEX_TOKEN=your_oauth_token_here
```

## Настройка Yandex OAuth Token

1. Перейдите на [Yandex OAuth](https://yandex.ru/dev/disk/rest/)
2. Создайте приложение
3. Получите OAuth токен
4. Добавьте токен в файл `.env`

## Структура проекта

```
├── main.py                 # Основной файл приложения
├── templates/
│   └── index.html         # Шаблон главной страницы
├── static/
│   └── style.css          # CSS стили
├── temp/                  # Временная директория для файлов
├── requirements.txt       # Зависимости проекта
└── .env                   # Конфигурационный файл
```

## Запуск приложения

1. Активируйте виртуальное окружение:
```bash
source .venv/bin/activate  # для Linux/MacOS
.venv\Scripts\activate     # для Windows
```

2. Запустите Flask-приложение:
```bash
python main.py
```

3. Откройте браузер и перейдите по адресу: `http://localhost:5000`

## API Endpoints

### GET /
- Главная страница с формой для ввода публичной ссылки

### POST /
- Обработка формы и отображение списка файлов
- Параметры формы:
  - `public_key`: Публичная ссылка Яндекс.Диска
  - `filter_type`: Тип фильтра (0 - все файлы, documents - документы, images - изображения)

### GET /download_single/<path:file_path>
- Скачивание отдельного файла
- Параметры:
  - `file_path`: URL файла на Яндекс.Диске

## Поддерживаемые форматы файлов

### Документы
- doc, docx (Microsoft Word)
- pdf (Adobe PDF)
- txt (Текстовые файлы)
- xlsx, xls (Microsoft Excel)

### Изображения
- jpg, jpeg
- png
- gif
- svg

## Обработка ошибок

- Неверный токен: Проверьте правильность OAuth токена в файле `.env`
- Недоступная ссылка: Убедитесь, что публичная ссылка действительна
- Ошибки скачивания: Проверьте доступность файлов и права доступа


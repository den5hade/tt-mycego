from flask import Flask, render_template, request, send_from_directory
import urllib
import os
import requests
import datetime
from zipfile import ZipFile
from dotenv import load_dotenv

load_dotenv()  # получаем переменные из .env.

# Настройка приложения Flask
app = Flask(__name__)

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")

# Точка входа
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        public_key = request.form['public_key']
        filter_type = request.form.get('filter_type')
        
        # Получение списка файлов с Яндекс.Диска
        try:
            resources = get_public_resources(public_key, filter_type)

            return render_template('index.html', files=resources, success=True)
        except Exception as e:
            print(e)
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

# Функция для получения списка файлов по публичной ссылке
def get_public_resources(public_key: str, filter_type: str = None) -> list:
    # Формируем URL для API запроса к Яндекс.Диску
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
    headers = {'Authorization': YANDEX_TOKEN}
    
    # Отправляем GET запрос к API Яндекс.Диска
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        resources = response.json()
    else:
        raise Exception(f'Ошибка при запросе к API: {response.text}')

    # Если выбран тип фильтра (не "Все файлы")
    if filter_type != '0':
        # Определяем допустимые расширения файлов в зависимости от типа фильтра
        if filter_type == 'documents':
            allowed_extensions = ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'xls']
        elif filter_type == 'images':
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'svg']
        else:
            allowed_extensions = []
        
        # Фильтруем файлы по типу и расширению
        filtered_files = [
            resource for resource in resources['_embedded']['items']
            if resource['type'] == 'file'  # Проверяем, что это файл, а не папка
               and any(resource['name'].endswith(ext) for ext in allowed_extensions)  # Проверяем расширение файла
        ]

        return filtered_files

    # Если фильтр не выбран, возвращаем все элементы
    return resources['_embedded']['items']

@app.route('/download_single/<path:file_path>')
def download_single(file_path):
    try:
        # Создайте временный каталог, если он не существует
        temp_dir = os.path.join(app.root_path, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Скачайте файл с Яндекс.Диска
        headers = {'Authorization': YANDEX_TOKEN}
        response = requests.get(file_path, headers=headers)
        
        if response.status_code == 200:
            # Получите оригинальное имя файла из URL
            # filename = os.path.basename(urllib.parse.unquote(file_path))
            real_name = file_path.split('&')
            for i in real_name:
                if i.startswith('filename'):
                    file_name = i.split('=')[-1]
            
            # Сохраните файл временно
            temp_file_path = os.path.join(temp_dir, file_name)
            with open(temp_file_path, 'wb') as f:
                f.write(response.content)
            
            # Отправьте файл пользователю
            try:
                return send_from_directory(
                    directory=temp_dir,
                    path=file_name,
                    as_attachment=True,
                    download_name=file_name
                )
            finally:
                # Очистите временный файл после отправки
                try:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                except:
                    pass
        else:
            return f'Failed to download file: {response.status_code}', 500
            
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)

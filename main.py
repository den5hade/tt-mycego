from flask import Flask, render_template, request, send_from_directory
import urllib
import os
import requests
import datetime
from zipfile import ZipFile

# Настройка приложения Flask
app = Flask(__name__)

YANDEX_TOKEN = "y0__xCd9qCYBBjblgMg94fuuxIHlDbflgaAC7N1KdWWJ-0ETOoWgQ"

public_key = YANDEX_TOKEN

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
def get_public_resources(public_key, filter_type=None):
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
    headers = {'Authorization': publick_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        resources = response.json()
    else:
        raise Exception(f'Ошибка при запросе к API: {response.text}')
    
    # if filter_type is not None:
    #     if filter_type == 'documents':
    #         allowed_extensions = ['doc', 'docx', 'pdf', 'txt']
    #     elif filter_type == 'images':
    #         allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    #     else:
    #         allowed_extensions = []
        
    #     filtered_files = [
    #         resource for resource in resources['items']
    #         if resource['media_type'] == 'file'
    #            and any(resource['name'].endswith(ext) for ext in allowed_extensions)
    #     ]
    #     return {'items': filtered_files}

    return resources['_embedded']['items']


if __name__ == '__main__':
    app.run(debug=True)
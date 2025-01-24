import os
import time
import zipfile
import tarfile
from pathlib import Path

import rarfile
import requests


def download(host_ip, save_path):
    url = f'http://{host_ip}/{file_name}'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True, allow_redirects=False)
        response.raise_for_status()
        print(response.url)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"Файл успешно скачан: {save_path}")
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")


def extract_archive(file_path, extract_to):
    try:
        _, ext = os.path.splitext(file_path)
    except FileNotFoundError as e:
        print('Файл не найден!')

    try:
        if ext == '.zip':
            with zipfile.ZipFile(file_path, 'r') as archive:
                archive.extractall(extract_to, pwd=password.encode('utf-8'))
                print(f'ZIP-файл извлечён в {extract_to}')

        elif ext in ['.tar', '.gz', '.bz2', '.xz']:
            with tarfile.open(file_path, 'r:*') as archive:
                archive.extractall(extract_to)
                print(f'TAR-файл извлечён в {extract_to}')

        elif ext == '.rar':
            with rarfile.RarFile(file_path, 'r') as archive:
                archive.extractall(extract_to, pwd=password)
                print(f'RAR-файл извлечён в {extract_to}')

        else:
            print(f'Формат {ext} не поддерживается.')

    except Exception as e:
        print(f'Ошибка при извлечении: {e}')


host_ip = input('Введите айпи хоста на котором лежит файл: ')
file_name = input('Укажите имя и расширение файла в формате <имя_файла>.<расширение>: ')
password = input('Укажите пароль для архива: ')

archive_path = os.path.join(os.getenv('APPDATA'), file_name)
destination_path = f'{Path.home()}/Desktop/test_task6/'

download(host_ip, archive_path)
extract_archive(archive_path, destination_path)

for root, dirs, files in os.walk(destination_path):
    for file in files:
        ext = file.split('.')[-1]

        if ext == 'exe':
            print(f'Будет выполнен распакованный файл {file}')
            time.sleep(5)
            os.system(f'{destination_path}/{file}')

input('Нажмите ENTER чтобы выйти... ')

import hashlib
import os
from pathlib import Path

import psutil
import pyzipper
from telethon import TelegramClient


api_id = int(input('Введите API ID: '))
api_hash = input('Введите API Hash: ')

client = TelegramClient('session', api_id, api_hash)
channel_name = 'test_task_4'

home_directory = Path.home()
required_file_name = 'test.zip'
downloaded_file = f'{home_directory}/{required_file_name}'


def get_file_from_chat():
    def extract_protected_zip(zip_path, extract_to):
        try:
            with pyzipper.AESZipFile(zip_path, 'r') as zip_ref:
                password = input('Введите пароль для архива (123): ')
                zip_ref.extractall(extract_to, pwd=password.encode('utf-8'))
                print(f'Успешно разархивировано')
        except Exception as e:
            print(f'Ошибка: {e}')

    zip_file_path = downloaded_file
    destination_folder = home_directory

    async def main():
        async for message in client.iter_messages(channel_name, limit=10):
            if message.file and message.file.name == required_file_name:
                print(f'Скачивание {required_file_name}...')
                await message.download_media(downloaded_file)
                print('Файл успешно скачан, разархивирование...')
                extract_protected_zip(zip_file_path, destination_folder)

    with client:
        client.loop.run_until_complete(main())


def get_hash_from_telegram():
    async def main():
        hash_from_telegram = (await client.get_messages(channel_name, limit=1))[0].message
        return hash_from_telegram
    with client:
        hash_from_telegram = client.loop.run_until_complete(main())
        return hash_from_telegram


def stop_process_by_name(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if process.info['name'].lower() == process_name.lower():
                process.terminate()
                print(f'Работа write.exe была завершена. Хэши не совпадают')
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def check_hashes():
    def calculate_sha256(file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    file_path = downloaded_file
    file_hash = calculate_sha256(file_path)
    hash_from_telegram = get_hash_from_telegram()

    if file_hash != hash_from_telegram:
        print('Хэши не совпадают, удаление архива и приложений...')
        try:
            stop_process_by_name('write.exe')
            os.remove(f'{home_directory}/test.zip')
            os.remove(f'{home_directory}/write.exe')
            os.remove(f'{home_directory}/hash.exe')
        except Exception as e:
            pass
        print('Успешно удалено')
        get_file_from_chat()
        input('Нажмите ENTER для выхода')
    else:
        print('Хэши совпадают, проверка успешна')
        input('Нажмите ENTER для выхода')


check_hashes()

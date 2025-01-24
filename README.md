# Тестовые задания


## Задание 1: Развертывание веб-сервера и создание паролированного архива с хеш-значением
### Описание задачи
1. Развернуть веб-хост http://localhost на локальном компютере используя веб сервер (apache или nginx или IIS) и разместить на нем 
   паролированный архив test.zip 
   который содержит исполняемый файл write.exe и PowerShell скрипт hash.ps1, а также разместить веб-страницу index.html которая 
   содержит вычисленное хеш-значение файла test.zip по алгоритму SHA256
2. В PowerShell скрипте hash.ps1 необходимо реализовать: 
    а) сравнение хеш-значения загруженного файла test.zip со значением из веб страницы
    b) остановку работы write.exe, удаление разархивированных файлов write.exe и hash.ps1, а также архива test.zip, если 
       хеш-значения не совпадают
    с) выполнение действий в пунктах 3.1, 3.2
3. Создать PowerShell скрипт main.ps1 которая выполняет следующие действия:
    3.1 Скачивает архивированный файл test.zip
    3.2 Разархивирует содержание архива test.zip в домашнюю директорию пользователя
    3.3 Вносит в "Планировщик задач" новую задачу с названием TimeToWrite, которая ежедневно в 12:00 будет запускать 
        разархивированный файл write.exe и PowerShell скрипт hash.ps1


### Шаги выполнения
1. Развертывание веб-сервера
Для выполнения задания использован Nginx, развернутый в Docker контейнере. Для этого использован внешний IP адрес, так как доступ через localhost не был возможен. Nginx настроен для раздачи архива test.zip по адресу http://<IP>/test.zip.
2. Создание веб-страницы 
Веб-страница - `task1/index.html` содержит вычисленное хеш-значение файла test.zip по алгоритму SHA256. 
3. PowerShell скрипт `task1/hash.ps1`
Скрипт проверяет хеш-значение загруженного архива с тем, что указано на веб-странице. В случае несоответствия хешей, выполняется остановка процесса write.exe, удаление всех файлов (архива, скриптов) и повторная загрузка архива.
4. PowerShell скрипт `task1/main.ps1`
Скрипт берет IP адрес интерфейса Ethernet 2 и подставляет под строку http://<IP>/test.zip, после чего отправляется запрос для сохранения файла test.zip в домашней директории пользователя с дальнейшим его разархивированием. После разархивации скрипт вносит в "Планировщик Задач" два разархивированных файла - `task1/hash.ps1` и `write.exe`, они будут выполняться ежедневно в 12:00.


### Как запустить
1. Если есть Docker Desktop, заходим в него и авторизуемся (если нет, скачиваем через [официальный сайт](https://www.docker.com/products/docker-desktop/). После, в терминале вводим `docker pull even098/test_task_1_2:latest` для пулла image nginx сервера. Нажимаем на кнопку "Запустить", в дополнительных параметрах ставим Host port на 80 и любое имя. 
2. После запуска контейнера, скачиваем - `task1/main.ps1` и запускаем через **Windows Powershell ISE**.
3. Для проверки работоспособности, можно в файлах nginx изменить значение хэша в index.html, который лежит по пути `/usr/share/nginx/html/` и самостоятельно запустить `hash.ps1`.

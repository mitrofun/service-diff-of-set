# Тестовое задание Perx Soft

[![Build Status](https://www.travis-ci.com/mitrofun/service-diff-of-set.svg?branch=master)](https://www.travis-ci.com/mitrofun/service-diff-of-set)

## Описание

Реализовать веб-приложение, которое предоставляет API со следующим функционалом:
- возможность загрузить и обработать файл в формате excel
- возможность получить статус обработки загруженного файла, который должен включать следующую информацию:
    - дата и время загрузки
    - дата и время окончания обработки, если обработка завершена
    - статус обработки (загружено, обрабатывается, обработано)
    - результат обработки
- API должен быть защищён авторизацией
    - авторизация должна производиться с помощью токена или пары имя пользователя, пароль
    - в базе данных эти данные, используемые для авторизации, хранить не требуется

О структуре загружаемого файла
- загружаемый файл представляет собой файл Excel (xls или xlsx)
- файл состоит из нескольких листов, каждый из которых имеет свой набор колонок или не имеет вообще никаких данных
- количество колонок, а также их порядок не фиксирован
- в первой строке указаны заголовки колонок
- последней колонкой на листе считается та, у которой справа от её заголовка находится пустая ячейка
- данные в колонке также ограничены пустой ячейкой снизу
- на одном из листов содержатся колонки с заголовками before и after
- далее речь идёт о только колонках before и after
- одна из колонок содержит список L1 из N положительных целых чисел
- другая колонка содержит список L2 из N+1 положительных целых чисел
- известно, что набор из L2 состоит из набора L1 и ещё некоего числа X
- порядок следования общих чисел в наборах может различаться

Что необходимо сделать в процессе обработки:
- необходимо определить число X
- если набор L1 находился в колонке before, то в результат обработки поместить `added: X`
- если набор L1 находился в колонке after, то в результат обработки поместить `removed: X`
- время обработки должно быть линейным

Приложение может быть реализовано с использованием любого фреймворка. Для определения числа X нельзя использовать специализированные библиотеки обработки данных, такие как pandas. Дополнительным плюсом будет размещение приложения в контейнере Docker. Разработанное приложение необходимо размесить в github-репозитории.

# Зависимости
- python 3.9+
- fastapi
- sqlite
- docker
- docker-compose
- mypy
- flake8
- pytest

# Установка

## Локальная установка
- Клонируем 
```bash
git clone https://github.com/mitrofun/service-diff-of-set.git
```
- Создаем необходимые переменные окружения для работы приложения
```bash
cd service-diff-of-set
cp example.env config.env
```
- Создаем виртуальное окружение и активируем его
```bash
virtualenv .venv
source .venv/bin/activate
```
- Устанавливаем poetry и зависимости проекта
```bash
pip install poetry && poetry install
```
- Создать папку для базы данных
```bash
mkdir data
```
- Выполнить миграции
```bash
alembic upgrade head
```  
- Запуск приложения
```bash
uvicorn src.main:app --reload
```
## Алиасы для локальной разработки
- Запуск миграций
```bash
make migration  
```
- Запуск локального сервера разработки
```bash
make run  
```
- Запуск линтера
```bash
make linter  
```
- Запуск тестов
```bash
make qa  
```

## Установка и запуск через docker-compose
- Клонируем 
```bash
git clone https://github.com/mitrofun/service-diff-of-set.git
```
- Создаем необходимые переменные окружения для работы приложения
```bash
cd service-diff-of-set
cp example.env config.env
```
- Запускаем docker-compose 
```bash
docker-compose up
```

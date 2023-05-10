# big_data_library
Тестовое задание для курса «Хранилища данных. Введение в большие данные»
## Установка
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Команды для работы
### Вывести кол-во книг находящихся на руках у всех читателей на момент конкретной даты
`python3 main.py get_readers_books --date 2022-10-01`
### Вывести кол-во книг находящихся на руках у всех читателей
`python3 main.py get_readers_books`
### Предпочитаемый жанр для конкретного читетеля
`python3 main.py get_prefer_reader_genre --reader "Д.П.Лазарев"`
### Список предпочитаемых жанров для всех читетелей
`python3 main.py get_prefer_reader_genre

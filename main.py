import argparse
import psycopg2
from datetime import date

get_readers_books_query = '''
    select r.name, count(*) filter(where book_id is not null) 
    from (
    	select reader_id, book_id from history h 
    	where (return_date > %(dt)s or return_date is null) and recive_date <= %(dt)s
    ) reader_books
    right join readers r on reader_books.reader_id = r.reader_id
    group by r.name 
'''
get_prefer_book_query = '''
with genres_info as (
	select reader_id, g.genre_id, count(*) as cnt
	 from (
    	select reader_id, book_id from history h 
    	where (return_date > now() or return_date is null) and recive_date <= now()
    ) reader_books
	join book_genres bg on bg.book_id = reader_books.book_id
	join genres g  on g.genre_id = bg.genre_id
	group by reader_id, g.genre_id 
)

select r.name, g.name, cnt 
from genres_info
join readers r on genres_info.reader_id = r.reader_id 
join genres g on genres_info.genre_id = g.genre_id 
where 
    (genres_info.reader_id, cnt) in (select reader_id, max(cnt) 
    from genres_info group by reader_id) 
    and (
        cardinality(%(readers)s::varchar[]) > 0
        and r.name = ANY(%(readers)s::varchar[]) or cardinality(%(readers)s::varchar[]) = 0
    )
order by r.name
'''

connect = psycopg2.connect(
    user='postgres',
    password='postgres',
    database='library',
    host='localhost',
)

def get_readers_books(date = date.today()):
    cursor = connect.cursor()    
    cursor.execute(get_readers_books_query, {'dt':date})
    rows = cursor.fetchall()
    print('{:>15}|{:>15}|'.format('Читатель', 'Кол-во книг'))
    print('-'*30)
    print(
        '\n'.join(['{:>15}{:>15}'.format(*row) for row in rows])
    )

def get_prefer_reader_genre(readers = []):
    cursor = connect.cursor()
    cursor.execute(get_prefer_book_query, {'readers':readers})
    rows = cursor.fetchall()
    print('{:>15}|{:>15}|{:>10}|'.format('Читатель', 'Жанр', 'Кол-во'))
    print('-'*40)
    print(
        '\n'.join(['{:>15}{:>15}{:>10}'.format(*row) for row in rows])
    )


def handle_parser_comand(args):
    if args.command == 'get_readers_books':
        get_readers_books(args.date)
    elif args.command == 'get_prefer_reader_genre':
        readers = [reader for reader in args.reader.split(', ') if reader]
        get_prefer_reader_genre(readers)

    


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Команда для работы с библиотекой')
    parser.add_argument('command', choices=['get_readers_books', 'get_prefer_reader_genre'], help='Выбирете команду')
    parser.add_argument('--date', type=str, default=date.today(), help='Введите на какую дату вы хотите получить информацию')
    parser.add_argument('--reader', type=str, default='', help='Чтобы получить любимый жанр конкретного читателя - введите его')
    args = parser.parse_args()
    handle_parser_comand(args)

    
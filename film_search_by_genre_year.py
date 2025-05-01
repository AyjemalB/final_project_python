from db import conn_read, cursor_read
from tabulate import tabulate
from keyword_logging import log_search

# Получаем все жанры
query_genre = 'SELECT name FROM category'
cursor_read.execute(query_genre)
rows = [genre[0] for genre in cursor_read.fetchall()]
genres_set = set(g.lower() for g in rows)  # для проверки без учета регистра

def search_genre_and_year():
    while True:
        # --- Выбор жанра ---
        while True:
            genre_input = input(f'Available genres:\n{rows}\nWhich one do you want to search: ').strip().lower()
            if genre_input in genres_set:
                genre = next(g for g in rows if g.lower() == genre_input)
                break
            else:
                print("❗ Invalid genre. Please try again.\n")

        # --- Ввод года с оператором ---
        while True:
            year_input = input("Enter the release year to search for (example: >2005, <2010, =2008): ").strip()
            if year_input and (year_input[0] in ['<', '>', '=']) and year_input[1:].isdigit():
                operator = year_input[0]
                year = int(year_input[1:])
                break
            else:
                print("❗ Invalid input. Please use format like '>2005', '<2010', '=2008'.")

        # --- SQL-запрос ---
        query_genre_and_year = f'''
            SELECT film.title, film.release_year, category.name, film.length
            FROM film
            INNER JOIN film_category ON film.film_id = film_category.film_id
            INNER JOIN category ON film_category.category_id = category.category_id
            WHERE category.name = %s AND film.release_year {operator} %s
        '''
        cursor_read.execute(query_genre_and_year, (genre, year))
        results = cursor_read.fetchall()

        log_search('genre_year', f'{genre} {operator}{year}')

        if results:
            headers = ["🎬 Title", "🗓️ Year", "🎭 Genre", "⏳ Length (min)"]
            start = 0
            page_size = 10

            while start < len(results):
                end = start + page_size
                print(tabulate(results[start:end], headers=headers, tablefmt="fancy_grid"))
                start = end

                if start < len(results):
                    more = input("Do you want to see more? (y/n): ").strip().lower()
                    if more not in ("yes", "y"):
                        print("✅ Search finished.")
                        break
                else:
                    print("✅ No more results.")
        else:
            print("❗ No films found for this genre and year.")

        # --- Повторный поиск? ---
        repeat = input("🔄 Do you want to search again? (yes/no): ").strip().lower()
        if repeat not in ("yes", "y"):
            break


# search_genre_and_year()







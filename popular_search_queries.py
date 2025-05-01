from db import get_db_edit_connection
from tabulate import tabulate

def fetch_popular_queries(limit=3):
    conn_write, cursor_write = get_db_edit_connection()
    query = '''
        SELECT query_text, query_cnt 
        FROM search_log 
        ORDER BY query_cnt DESC 
        LIMIT %s
    '''
    cursor_write.execute(query, (limit,))
    results = cursor_write.fetchall()
    return results


def show_popular_queries():
    # Отображает таблицу популярных запросов с возможностью поэтапного показа.
    limit = 3
    while True:
        # Получаем и выводим список популярных запросов
        popular = fetch_popular_queries(limit)
        table = [(i + 1, text, cnt) for i, (text, cnt) in enumerate(popular)]
        print(f"😎 Top {limit} most popular queries:")
        print(tabulate(table, headers=["#", "Query", "Count"], tablefmt="grid"))

        # Запрашиваем у пользователя, хочет ли он увидеть больше
        while True:
            user_input = input("Would you like to see more queries? (y/n): ").strip().lower()
            if user_input in ("yes", "y"):
                limit += 3  # Увеличиваем лимит для следующего вывода
                break
            elif user_input in ("no", "n"):
                return  # Завершаем вывод
            else:
                print("❗ Invalid input. Please enter 'yes' or 'no'.")




# Example call:
if __name__ == "__main__":
    show_popular_queries()


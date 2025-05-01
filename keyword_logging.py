from db import get_db_edit_connection
from datetime import datetime

def create_table():
    #Создание таблицы search_log.
    conn_write, cursor_write = get_db_edit_connection()

    cursor_write.execute("""
    CREATE TABLE IF NOT EXISTS search_log (
        search_type VARCHAR(50) NOT NULL,
        query_text VARCHAR(255) NOT NULL,
        query_cnt INT DEFAULT 1,
        last_queried TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (search_type, query_text)
    )
    """)
    conn_write.commit()
    print("Таблица search_log успешно создана.")

def log_search(search_type, query_text):
    #Запись логов в таблицу search_log.
    conn_write, cursor_write = get_db_edit_connection()

    check_query = """
        SELECT query_cnt FROM search_log
        WHERE search_type = %s AND query_text = %s
    """
    cursor_write.execute(check_query, (search_type, query_text))
    result = cursor_write.fetchone()

    if result:
        update_query = """
            UPDATE search_log
            SET query_cnt = query_cnt + 1, last_queried = %s
            WHERE search_type = %s AND query_text = %s
        """
        cursor_write.execute(update_query, (datetime.now(), search_type, query_text))
    else:
        insert_query = """
            INSERT INTO search_log (search_type, query_text, query_cnt, last_queried)
            VALUES (%s, %s, 1, %s)
        """
        cursor_write.execute(insert_query, (search_type, query_text, datetime.now()))

    conn_write.commit()


# create_table()


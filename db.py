import mysql.connector
import dotenv
from pathlib import Path
import os


dotenv.load_dotenv(Path('.env'))

# Настройки для подключения к базе данных для чтения
db_config_read = {'host': os.environ.get('host_read'),
            'user': os.environ.get('user_read'),
            'password': os.environ.get('password_read'),
            'database': 'sakila'
             }
# Подключение и курсор для чтения
conn_read = mysql.connector.connect(**db_config_read)
cursor_read = conn_read.cursor()




# Настройки для подключения к базе данных для записи (если нужно)
db_config_write = {'host': os.environ.get('host_write'),
            'user': os.environ.get('user_write'),
            'password': os.environ.get('password_write'),
            'database': 'group_111124_fp_AyjeamlB'
             }


# Подключение и курсор для записи
conn_write = mysql.connector.connect(**db_config_write)
cursor_write = conn_write.cursor()

def get_db_edit_connection():
    #Возвращает соединение и курсор для записи в базу данных.
    return conn_write, cursor_write




import mysql.connector
from db import conn_read, cursor_read
from tabulate import tabulate
from keyword_logging import log_search



def search_key_word():
    while True:
        key = input('Enter a keyword to search for: ').strip()

        # SQL query to search for films using LIKE
        query = "SELECT title, release_year, length FROM film WHERE title LIKE %s LIMIT %s, %s"
        wildcard_key = f"%{key}%"  # wrap the keyword with % for LIKE

        offset = 0  # To keep track of the number of records already displayed
        limit = 10  # Number of results per page

        while True:
            try:
                # Execute the query with the offset and limit
                cursor_read.execute(query, (wildcard_key, offset, limit))
                rows = cursor_read.fetchall()

                if rows:
                    print(f"Found {len(rows)} records:\n")

                    # Prepare the data for tabulation
                    table_data = [row for row in rows]
                    print(tabulate(table_data, headers=["🍿 Title", "🗓️ Year", "⏳ Length"], tablefmt="grid"))

                    user_input = input("Do you want to see more results? (y/n): ").strip().lower()
                    if user_input == 'y':
                        offset += limit
                    else:
                        print("Search completed.")
                        log_search('keyword', key) # Save key in db-edit
                        return  # End the function completely
                else:
                    print("No films found with that keyword. Please try again.\n")
                    break  # Ask for a new keyword

            except Exception as e:
                print(f"An error occurred during the search: {e}")
                return

# search_key_word()

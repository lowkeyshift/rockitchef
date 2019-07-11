import sqlite3
from sqlite3 import Error
from pathlib import Path
from TableCreation import TableCreation as tableC


# Pull name data from tables
def select_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

    rows = cur.fetchall()

    for row in rows:
        print(row)

# Pull data from recipes db
def select_recipes(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes;")

    rows = cur.fetchall()

    for row in rows:
        print(row)

# Pull data from directions_uncleaned
def select_directions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM directions_uncleaned;")

    rows = cur.fetchall()
    names = list(map(lambda x: x[0], cur.description))
    for row in rows:
        pk, fk, dirs = row
        print(dirs)
    print(names)

def main():
    database = "../crawler/rockit/rockit.db"
    database2 = "../crawler/rockit/rockit_clean.db"
    conn = sqlite3.connect(database)
    while True:
        try:
            print("file exists, updating {}".format(database))
            # create a database connection
            conn = create_connection(database2)
            with conn:
                print("Query select_directions")
                select_directions(conn)
                #print("Show tables")
                #select_tables(conn)
        except Error as e:
            init_tableC = tableC(conn)
            init_tableC.crawl_table()
            init_tableC.chefs_table()
            init_tableC.recipes_table()
            init_tableC.directions_table()
            init_tableC.ingredients_table()
            init_tableC.commit_close()
            continue
        break



if __name__ == '__main__':
    main()

# Classify Data with nltk and pattern match with re

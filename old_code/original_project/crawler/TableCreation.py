import sqlite3


class TableCreation:

    def __init__(self, conn):
        self.conn = conn

    # Crawled table
    def crawl_table(self):
        create_table_crawled = (
                    "CREATE TABLE crawled("
                    "id integer primary key autoincrement,"
                    "url text,"
                    "source text"
                    ");"
                )
        c = self.conn.cursor()
        c.execute(create_table_crawled)

    #chefs
    def chefs_table(self):
        create_table_chefs = (
                    "CREATE TABLE users("
                    "id integer primary key autoincrement,"
                    "url text,"
                    "name text"
                    ");"
                )
        c = self.conn.cursor()
        c.execute(create_table_chefs)

    # recipes
    def recipes_table(self):
        create_table_recipes = (
                    "CREATE TABLE recipes("
                    "id integer primary key autoincrement,"
                    "chef_id integer,"
                    "title text",
                    "url text,"
                    "prep_time text,"
                    "cook_time text,"
                    "tags text,"
                    "FOREIGN KEY(chef_id) REFERENCES users(id)"
                    ");"
                )
        c = self.conn.cursor()
        c.execute(create_table_recipes)

    # directions
    def directions_table(self):
        create_table_directions = (
                    "CREATE TABLE directions_uncleaned("
                    "id integer primary key autoincrement,"
                    "recipe_id integer,"
                    "directions_json text,"
                    "FOREIGN KEY(recipe_id) REFERENCES recipes(id)"
                    ");"
                )
        c = self.conn.cursor()
        c.execute(create_table_directions)

    # ingredients
    def ingredients_table(self):
        create_table_ingredients = (
                    "CREATE TABLE ingredients_uncleaned("
                    "id integer primary key autoincrement,"
                    "recipe_id integer,"
                    "ingredient_qty text,"
                    "FOREIGN KEY(recipe_id) REFERENCES recipes(id)"
                    ");"
                )
        c = self.conn.cursor()
        c.execute(create_table_ingredients)

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

import sqlite3
conn = sqlite3.connect('~/rockit/rockit.db')
c = conn.cursor()
# Crawled table
create_table_crawled = (
            "CREATE TABLE crawled("
            "id integer primary key autoincrement,"
            "url text,"
            "source text"
            ");"
        )
c.execute(create_table_crawled)

#users
create_table_users = (
            "CREATE TABLE users("
            "id integer primary key autoincrement,"
            "url text,"
            "name text"
            ");"
        )
c.execute(create_table_users)

# recipes
create_table_recipes = (
            "CREATE TABLE recipes("
            "id integer primary key autoincrement,"
            "chef_id integer,"
            "title text,",
            "url text,"
            "prep_time text,"
            "cook_time text,"
            "tags text,"
            "FOREIGN KEY(chef_id) REFERENCES users(id)"
            ");"
        )
c.execute(create_table_recipes)

# directions_uncleaned
create_table_directions_uncleaned = (
            "CREATE TABLE directions_uncleaned("
            "id integer primary key autoincrement,"
            "recipe_id integer,"
            "directions_json text,"
            "FOREIGN KEY(recipe_id) REFERENCES recipes(id)"
            ");"
        )
c.execute(create_table_directions_uncleaned)

# directions_uncleaned
create_table_ingredients_uncleaned = (
            "CREATE TABLE ingredients_uncleaned("
            "id integer primary key autoincrement,"
            "recipe_id integer,"
            "ingredient_qty text,"
            "FOREIGN KEY(recipe_id) REFERENCES recipes(id)"
            ");"
        )
c.execute(create_table_ingredients_uncleaned)
conn.commit()
conn.close()
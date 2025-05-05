from datetime import datetime 
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        #create table if doesnt exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            weight INTEGER NOT NULL,
            weight_unit TEXT NOT NULL,
            price REAL NOT NULL,
            price_unit TEXT NOT NULL,
            current_date TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sales_date TEXT NOT NULL,
            cake_name TEXT NOT NULL,
            cake_type TEXT NOT NULL, 
            cake_weight INTEGER NOT NULL,
            primary_price REAL NOT NULL,
            selling_price REAL NOT NULL              
            );""")
        self.connection.commit()
    
    def add_ingredient(self, name, weight, weight_unit, price, price_unit):
        current_date = datetime.now().strftime("%Y-%m-%d")
        try:
            self.cursor.execute("""
                INSERT INTO ingredients (name, weight, weight_unit, price, price_unit, current_date)
                VALUES (?, ?, ?, ?, ?, ?);""", (name, weight, weight_unit, price, price_unit, current_date))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"ingredient '{name}' already exists")
            return False
    
    def add_sales(self, sales_date, cake_name, cake_type, cake_weight, primary_price, selling_price):
        self.cursor.execute("""INSERT INTO sales_data (sales_date, cake_name, cake_type, cake_weight, primary_price, selling_price)
        VALUES (?, ?, ?, ?, ?, ?);""", (sales_date, cake_name, cake_type, cake_weight, primary_price, selling_price))
        self.connection.commit()
        
    def delete_ingredient(self, name):
        self.cursor.execute("DELETE FROM ingredients WHERE name = ?;", (name,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_ingredients(self, old_name, new_name, weight, weight_unit, price, price_unit):
        self.cursor.execute(""" 
            UPDATE ingredients
            SET name = ?, weight = ?, weight_unit = ?, price = ?, price_unit = ?, WHERE name = ?;""",
            (new_name, weight, weight_unit, price, price_unit, old_name))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def get_all_ingredients(self):
        self.cursor.execute("SELECT current_date, name, weight, weight_unit, price, price_unit FROM  ingredients;")
        return self.cursor.fetchall()
    
    def get_all_sales(self):
        self.cursor.execute("SELECT sales_date, cake_name, cake_type, cake_weight, primary_price, selling_price FROM sales_data ORDER BY sales_date ASC")
        return self.cursor.fetchall()

    def get_chosen_ingredient(self, name):
        self.cursor.execute("SELECT current_date, name, weight, weight_unit, price, price_unit FROM ingredients WHERE name = ?", (name,))
        return self.cursor.fetchone()
    
    def clear_data(self):
        self.cursor.execute("DELETE FROM ingredients")
        self.cursor.execute("DELETE FROM sales_data")
        self.connection.commit()
    
    def close_conn(self):
        self.connection.close()
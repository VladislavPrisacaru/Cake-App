import time
import os
from datetime import datetime 
import sqlite3
import pandas as pd

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
            price REAL NOT NULL,
            current_date TEXT NOT NULL
            );
        """)
        self.connection.commit()
    
    def add_ingredients(self, name, weight, price):
        current_date = datetime.now().strftime("%Y-%m-%d")
        try:
            self.cursor.execute("""
                INSERT INTO ingredients (name, weight, price, current_date)
                VALUES (?, ?, ?, ?);""", (name, weight, price, current_date))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"ingredient '{name}' already exists")
            return False
        
    def delete_ingredient(self, name):
        self.cursor.execute("DELETE FROM ingredients WHERE name = ?;", (name,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_ingredients(self, name, weight, price):
        self.cursor.execute(""" 
            UPDATE ingredients
            SET weight = ?, price = ?
            WHERE name = ?;""",
            (weight, price, name))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def get_all_ingredients(self):
        self.cursor.execute("SELECT current_date, name, weight, price FROM  ingredients;")
        return self.cursor.fetchall()
    
    def get_chosen_ingredient(self, name):
        self.cursor.execute("SELECT weight, price FROM ingredients WHERE name = ?", (name,))
        return self.cursor.fetchone()
    
    def clear_data(self):
        self.cursor.execute("DELETE FROM ingredients")
        self.connection.commit()
    
    def close_conn(self):
        self.connection.close()


class IngredientManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.existing_ingredient = None
        self.ingredient_data = None

    def get_ing_details(self):
        while True:
            try:
                weight = float(input("Weight in g: "))
                if weight < 0:
                    time.sleep(0.5)
                    print("Weight cant be less than 0, please try again. \n")
                else:
                    break
            except ValueError:
                time.sleep(0.5)
                print("Weight must be a number, try again. \n")  
                  
        while True: 
            try:
                price = float(input("Price in £: "))
                print()
                if price < 0:
                    time.sleep(0.5)
                    print("Price cant be less than 0. ")
                else:
                    break
            except ValueError:
                time.sleep(0.5)
                print("Price must be a number, try again. \n")
        return weight, price

    def add_ingredients(self):
        print("Enter 'done' to finish\n")
        while True:
            name = input("Enter name of the ingredient: ").strip().lower()
            if name == "done":
                time.sleep(0.5)
                print("Exiting the function. Ingredients saved! \n")
                break

            existing_ingredient = self.db_manager.get_chosen_ingredient(name)
            if existing_ingredient:
                time.sleep(0.5)
                print(f"'{name}' already added, try another one. ")
                continue    

            if not name:
                time.sleep(0.5)
                print("You must enter a valid ingredient name. ")
                continue
            
            weight, price = self.get_ing_details()

            self.db_manager.add_ingredients(name, weight, price)
            time.sleep(0.5)

    def display_ingredients(self, skip_q=False):
        self.ingredient_data = self.db_manager.get_all_ingredients()

        if self.ingredient_data:
            columns = ["Date", "Name", "Weight(g)", "Price(£)",]
            df = pd.DataFrame(self.ingredient_data, columns=columns)
            df["Name"] = df["Name"].str.capitalize()
            df.index += 1
            print(df.to_string(index=1, index_names=False, justify="right"))
        else:
            print("No ingredients found.")
            return

        if not skip_q:
            input("Press any key to go back. ")
            time.sleep(0.5)
        
    def delete_ingredients(self):
        print("Current ingredients.")
        print()
        self.display_ingredients(skip_q=True)

        ingredient_names = {row[1] for row in self.ingredient_data}

        while True:
            print("Enter 'cancel' to go back \n")
                
            name = input("Choose ingredient to delete: ").strip().lower()
            if name == "cancel":
                print("Going back to menu. ")
                time.sleep(1)
                return
            print()
            if name not in ingredient_names:
                time.sleep(0.5)
                print(f"'{name}' wasnt found, try again")
                continue
            else: 
                warning_choice = input(f"Are you sure you want to delete {name} ? Y/N: ").strip().lower()
                print()
                if warning_choice == "n":
                    print(f"{name} wasn't deleted, going back to menu. ")
                    time.sleep(1)
                    return
                elif warning_choice == "y":
                    self.db_manager.delete_ingredient(name)
                    print(f"{name} was deleted, going back to menu. ")
                    time.sleep(1)
                    return
                
    def update_ingredients(self):
        print("Enter 'done' to go back to the menu. \n")
        self.display_ingredients(skip_q=True)
        ingredient_names = {row[1] for row in self.ingredient_data}
        while True:
            name = input("Choose ingredient to update: ").strip().lower()

            if name == "done":
                print("Going back to the menu.")
                return  
            
            if name not in ingredient_names:
                print(f"'{name}' wasnt found, please try again. ")
            else:
                weight, price = self.get_ing_details()
                self.db_manager.update_ingredients(name, weight, price)
                print(f"'{name}' has been updated")
                continue

    def _check_password(self, password):
        while True:
            passwordQ = input("Enter password: ").lower()
            if passwordQ == password:
                return True
            elif passwordQ == "exit":
                return
            else:  
                time.sleep(0.5)
                print("password incorect, try again. ")

    def clear_data(self):
        print("Enter 'exit'  to go back to menu")
        del_choice = input("Are you sure you want to delete all ingredients? Enter 'yes' to confirm. ")
        if del_choice.lower() == "yes":
            if self._check_password("1"):
                self.db_manager.clear_data()
                print("All ingredients deleted, going back to menu. ")
                time.sleep(1)
        else:
            print("Going back to menu. ")

    def calculate_cake(self):
        print("Enter 'exit' to go back.")
        print()
        time.sleep(0.5)
        self.display_ingredients(skip_q=True)
        ingredient_names = {row[1] for row in self.ingredient_data}
        print("\n Choose ingredients that you want to add in your recipe. ")
        print("Enter 'calculate' when all ingredients are entered. ")
        print()
        recipe = []
        while True:
            name = input("Enter an ingredient to add: ").strip().lower()
            if name == "exit":
                print("Exiting function...")
                time.sleep(.5)
                return

            if name == "calculate":
                if len(recipe) < 2:
                    print("Add at least 2 ingredients. ")
                else:
                    print("Calculating")
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="")
                    print()
                    break
                continue
            
            if name not in ingredient_names:
                print("Ingredient not found please try again!!!!!!!!!!! \n")
                continue
            else:
                recipe.append((name, 0))

            weight = input("Amount to use of this ingredient in g: ")
            print()     
            if weight.lower() == "exit":
                print("Exiting function...")
                time.sleep(0.5)               
                return
            
            try:
                weight = int(weight)

                if weight < 0:
                    time.sleep(.5)
                    print("weight cant be less than 0, please try again. \n")
                else:
                    recipe[-1] = (name, weight)
            except ValueError:
                time.sleep(0.5)
                print("Weight must be a number, try again. \n")

        total = 0
        total_weight = 0

        for name, weight in recipe:
            result = self.db_manager.get_chosen_ingredient(name)

            if result:
                db_weight, db_price = result
                price_per_gram = db_price / db_weight
                price_per_ingredient = price_per_gram * weight
                total += price_per_ingredient
                total_weight += weight
            else: 
                print(f"'{name}' not found. ")
                print()
                input("Press any key to go menu. ")
        print(f"Total is £{round(total, 2)} and it weights {total_weight} grams.")
        print()
        input("Press any key to go menu. ")


def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')


db_manager = DatabaseManager("cakeshop.db")
ingredient_manager = IngredientManager(db_manager)

def recipe_menu():
    while True:
        clear_output()
        print("==========Recipe Menu==========")
        print("1.  [WIP] Add a recipe")
        print("2.  [WIP] Display all recipes")
        print("3.  [WIP] Calculate recipe cost")
        print("4.  Back to main menu")
        print("==============================")

        choice = input("Please choose an option (1 - 4). \n")

        match choice:
            case "1":
                clear_output()
                pass
            case "2":
                clear_output()
                pass
            case "3":
                clear_output()
                pass
            case "4":
                break
            case _:
                print("Not an available option, try again. ")
                time.sleep(1)

def ingredient_menu():
    while True:
        clear_output()
        print("==========Ingredient Menu==========")
        print("1. Add ingredients")
        print("2. Delete ingredient")
        print("3. Update ingredients")
        print("4. Display all ingredients")
        print("5. Clear data")
        print("6. Back to main menu")
        print("===================================")

        choice = input("Please choose an option (1 - 6). \n")

        match choice:
            case "1":
                clear_output()
                ingredient_manager.add_ingredients()
            case "2":
                clear_output()
                ingredient_manager.delete_ingredients()
            case "3":
                clear_output()
                ingredient_manager.update_ingredients()
            case "4":
                clear_output()
                ingredient_manager.display_ingredients()
            case "5":
                clear_output()
                ingredient_manager.clear_data()
            case "6":
                break
            case _:
                print("Not an available option, try again. ")
                time.sleep(1)

def main_menu():
    while True:
        clear_output()
        print("==========Cake Shop==========")
        print("1. Ingredient Management")
        print("2. Recipe Management")
        print("3. Calculate 1 cake")
        print("4. Exit")
        print("=============================")

        choice = input("Please choose an option (1 - 4). \n")

        match choice:
            case "1":
                clear_output()
                ingredient_menu()
            case "2":
                clear_output()
                recipe_menu()
            case "3":
                clear_output()
                ingredient_manager.calculate_cake()
            case "4":
                db_manager.close_conn()
                print("Exiting the program, bye.")
                time.sleep(1)
                break
            case _:
                print("Not an available option, try again. ")
                time.sleep(1)

main_menu()

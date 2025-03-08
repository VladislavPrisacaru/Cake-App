import json
import time
import os
from datetime import datetime 

#main menu
def menu():
    while True:
        clearOutput()
        print("----------Cake Shop-------")
        print("1. Add ingredients") #done  
        print("2. Delete ingredient") #done
        print("3. Update ingredients") #done
        print("4. Calculate 1 cake") #done  
        print("5. Clear data") #done            
        print("6. Display all ingredients") #done
        print("7. Exit") #done
    
        choice = input("Please choose an option (1 - 7). \n")
    
        if choice == "1":
            clearOutput()
            addIngredients()
        elif choice == "2":
            clearOutput()
            deleteIngredients()
        elif choice == "3":
            clearOutput()
            updateIngredient()
        elif choice == "4":
            clearOutput()
            calculateCake()
        elif choice == "5":
            clearOutput()
            clearData()
        elif choice == "6":
            clearOutput()
            displayIngredients()
        elif choice == "7":
            print("exiting the program, bye.")
            time.sleep(1)
            print(ingredients)
            time.sleep(10)
        else:
            print("Not an available option, try again. ")

def clearOutput():
    os.system('cls' if os.name == 'nt' else 'clear')

#check password
def checkPassword(password):
    while True:
        passwordQ = input("Enter password: ")
        if passwordQ == password:
            return True
        elif passwordQ.lower() == "exit":
            return
        else:  
            time.sleep(0.5)
            print("password incorect, try again. ")
            
#load ingredients from json file
def loadIngredients():
    try:
        with open("ingredients.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
        
#save to the ingredients dict
def saveIngredients():
    with open("ingredients.json","w") as file: 
        json.dump(ingredients, file)
    
#clear all exising data
def clearData():
    print("Enter 'exit'  to go back to menu")
    delChoice = input("Are you sure you want to delete all ingredients? Enter 'yes' to confirm. ")
    if delChoice.lower() == "yes":
        if checkPassword("1"):
            with open("ingredients.json", "w") as file:
                json.dump({}, file)  
            global ingredients  
            ingredients = {}
            print("All ingredients deleted, going back to menu. ")
            time.sleep(1)
    else:
        print("Going back to menu. ")

#load data into the fil
ingredients = loadIngredients()

def getIngDetails():
    while True:
        try:
            ingWeight = float(input("Weight in g: "))
            if ingWeight < 0:
                time.sleep(.5)
                print("weight cant be less than 0, please try again. \n")
            else:
                break
        except ValueError:
            time.sleep(.5)
            print("Weight must be a number, try again. \n")  
    #get ingredient price           
    while True: 
        try:
            ingPrice = float(input("Price in £: "))
            print()
            if ingPrice < 0:
                time.sleep(.5)
                print("Price cant be less than 0. ")
            else:
                break
        except ValueError:
            time.sleep(.5)
            print("Price must be a number, try again. \n")
    return ingWeight, ingPrice

currentTime = datetime.now().strftime("%Y-%m-%d")

#add new ingredients to the ngredients dict
def addIngredients():
    print("Enter 'done' to finish\n")
    while True:
        ingName = input("Enter name of the ingredient: ").strip()
        if ingName.lower() == "done":
            time.sleep(.5)
            print("Exiting the function. Ingredients saved! \n")
            break

        if ingName in ingredients:
            time.sleep(.5)
            print("Ingredient already added, try another one. ")
            continue    

        if not ingName:
            time.sleep(0.5)
            print("You must enter a valid ingredient name. ")
            continue
        
        ingWeight, ingPrice = getIngDetails()
        
        if currentTime not in ingredients:
            ingredients[currentTime] = {}

        ingredients[currentTime][ingName] = {"weight" : ingWeight, "price" : ingPrice}
        saveIngredients()
        time.sleep(0.5)

#show all ingredients in order
def displayIngredients(skipQ=False):
    if not ingredients:
        print("No ingredients added. ")
        time.sleep(2)
        return False
    else:
        print(f"{"Date":<15} {"Ingredient":<15} {"Weight (g)":<15} {"price (£)":<15}")
        print("-" * 60)

        for times, ingData in ingredients.items():
            for ingredient, subDict in ingData.items():
                weight = subDict.get("weight", "N/A")
                price = subDict.get("price", "N/A")
                print(f"{times:<15} {ingredient:<15} {weight:<15} {price:<15} ")
        print()

    if not skipQ:
        input("Press enter to go back.")
        time.sleep(0.5)
               
#delete ingredient
def deleteIngredients():
    print("Current ingredients.")
    print()
    displayIngredients(skipQ=True)

    while True:
        print("Enter 'cancel' to go back")
        if not ingredients:
            time.sleep(0.5)
            print("No ingredients to delete. ")
            return
            
        ingName = input("Choose ingredient to delete: ")
        if ingName.lower() == "cancel":
            print("Going back to menu. ")
            time.sleep(2)
            return
        print()
        for Date, ingData in ingredients.items():
            if ingName not in ingData:
                time.sleep(2)
                print("Ingredient not found, try again. ")
                continue
            else: 
                warningChoice = input(f"Are you sure you want to delete {ingName} ? Y/N: ")
                print()
                if warningChoice.upper() == "N":
                    print(f"{ingName} wasn't deleted. ")
                    return
                elif warningChoice.upper() == "Y":
                    del ingData[ingName]
                    print(f"{ingName} was deleted, going back to menu. ")
                    time.sleep(2)
                    saveIngredients()
                    return
        time.sleep(0.5)
                
#update existing ingredients
def updateIngredient():
    print("Enter 'done' to go back to the menu.")
    displayIngredients(skipQ=True)
    while True:
        ingName = input("Choose ingredient to update: ")

        if ingName.lower() == "done":
            print("Going back to the menu.")
            return  
        
        found = False
        for Date, ingData in ingredients.items():
            if ingName in ingData:
                found = True
                ingWeight, ingPrice = getIngDetails()

                if currentTime not in ingredients:
                    ingredients[currentTime] = {}

                ingredients[currentTime][ingName] = {"weight" : ingWeight, "price" : ingPrice}
                saveIngredients()
                print(f"{ingName} has been updated.")
                break  

        if not found:
            time.sleep(2)
            print("Ingredient not found, try again.")
            continue
    
def calculateCake():
    print("Enter 'exit' to go back.")
    print()
    time.sleep(0.5)
    if displayIngredients(skipQ=True) == False:
        return
    print("Choose ingredients that you want to add in your recipe. ")
    print("Enter 'calculate' when all ingredients are entered. ")
    print()
    recipe = []
    while True:
        ingredientChoice = input("Enter an ingredient to add: ")
        if ingredientChoice.lower() == "exit":
            print("Exiting function...")
            time.sleep(.5)
            return

        if ingredientChoice.lower() == "calculate":
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

        found = False
        for Date, ingData in ingredients.items():
            if ingredientChoice in ingData:
                found = True 
                break

        if not found:
            print("Ingredient not found please try again!!!!!!!!!!! \n")
            continue

        recipe.append((ingredientChoice, 0))

        weightChoice = input("Amount to use of this ingredient in g: ")
        print()     
        if weightChoice.lower() == "exit":
            print("Exiting function...")
            time.sleep(.5)               
            return
        
        try:
            weightChoice = float(weightChoice)

            if weightChoice < 0:
                time.sleep(.5)
                print("weight cant be less than 0, please try again. \n")
            else:
                recipe[-1] = (ingredientChoice, weightChoice)
        except ValueError:
            time.sleep(.5)
            print("Weight must be a number, try again. \n")

    total = 0
    totalWeight = 0
    for ingredient, weight  in recipe:
        pricePerGram = ingredients[Date][ingredient]["price"] / ingredients[Date][ingredient]["weight"]
        pricePerIng = pricePerGram * weight
        total += pricePerIng
        totalWeight += weight
    print(f"Total is £{round(total, 2)} and it weights {totalWeight} grams.")
    print()
    input("Press any key to go menu. ")
        
menu()
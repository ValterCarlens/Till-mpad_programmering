'''
PRODUKTLAGER.PY: Produktlager där man kan hantera produkter via CSV fil.

__author__  = "Valter Carlens"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se"
'''

import csv
import os
import locale
import time
from colors import bcolors

# Product class
class Product:
    def __init__(self, id, name, desc, price, quantity) -> None:
        self.id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity

    def __str__(self):
        # Limits for strings 
        shortened_name = (self.name[:40] + '...') if len(self.name) > 40 else self.name
        shortened_desc = (self.desc[:35] + '...') if len(self.desc) > 35 else self.desc
        
        # Print each field with spacing
        return f"{self.id:<5} {shortened_name:<45} {shortened_desc:<40} {locale.currency(self.price, grouping=True):<15} {self.quantity:<8}"
    
# Inventory class to manage products
class Inventory:
    def __init__(self, filename:str) -> None:
        self.products = []
        self.filename = filename

    # Add product method 
    def add(self, product:Product) -> None:
        new_id = 1
        if len(self.products) > 0:
            # Returns the biggest product.id + 1
            new_id = max([product.id for product in self.products]) + 1 
        product.id = new_id
        self.products.append(product)

        # Append the new product to the CSV file
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product.id, product.name, product.desc, product.price, product.quantity])
    
    # Write products to the CSV file
    def save_data(self) -> None:
        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ["id","name","desc","price","quantity"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for product in self.products:
                writer.writerow([product.id, product.name, product.desc, product.price, product.quantity])

    # Append to the productslist and give each product properties id, name, desc, price, quantity
    def load_data(self) -> None:
        self.products = []
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    id = int(row['id'])
                    name = row['name']
                    desc = row['desc']
                    price = float(row['price'])
                    quantity = int(row['quantity'])
                    
                    self.products.append(Product(id, name, desc, price, quantity))
        except:
            print("The csv file does not exist")
            exit()

    # Remove desired product
    def remove(self, id:int ) -> Product:
        removed_product:Product = None
        for i in range(len(self.products)) :
            prod = self.products[i]
            if prod.id == id:
                removed_product = self.products[id]
                del self.products[id]
                break
        self.save_data()
        return removed_product

def print_products():
    header = f"{'ID':<5} {'NAME':<45} {'DESCRIPTION':<40} {'PRICE':<15} {'QUANTITY':<8}"
    separator_top = "-" * 115  
    seperator_bottom = "-" * 115
    
    print(bcolors.YELLOW + header)
    print(bcolors.CYAN + separator_top)
    
    # Print each product
    for product in inventory.products:
        print(bcolors.GREEN + f"{product}")
    print(bcolors.CYAN + seperator_bottom)

# User input for new product
def new_product_dialog() -> Product:
    name = input("Product_Name: ")
    desc = input("Product_Description: ")
    price = float(input("Product_Price: "))
    quantity = int(input("Product_Quantity: "))
    return Product(None, name, desc, price, quantity)

# Remove product
def remove_product_dialog() -> Product:
    print_products()
    try:
        user_remove = int(input(bcolors.YELLOW + f"What product would you like to remove?\nEnter id: "))
        if user_remove in [product.id for product in inventory.products]:
            removed_product = inventory.remove(user_remove - 1)
            print(f"Removed {removed_product.name}")
            time.sleep(4)
            return removed_product
        else:
            print(bcolors.RED + "Number is out of range")
            time.sleep(1.5)
    except ValueError:
        print(bcolors.RED + "Invalid_input")
        time.sleep(1.5)
        return None
    
# User input to change product
def change_product_dialog() -> Product:
    print_products()
    user_change_product= input(bcolors.YELLOW + "What product would you like to change? (q to quit)\nEnter ID: ")
    if user_change_product == "q":
        return None

    try:
        user_change_product_id= int(user_change_product)
        for product in inventory.products:
            if user_change_product_id == product.id:
                print(bcolors.CYAN + f"currently editing {product.name}\nleave space empty to skip")
                product.name = input(bcolors.DEFAULT + f"Enter new name [{product.name}]:") or product.name
                product.desc = input(bcolors.DEFAULT + f"Enter new description [{product.desc}]:") or product.desc
                product.price = input(bcolors.DEFAULT + f"Enter new price [{product.price}]:") or product.price
                product.quantity = input(bcolors.DEFAULT + f"Enter new quantity [{product.quantity}]:") or product.quantity
                float(product.price)
                float(product.quantity)
                inventory.save_data()
                return product
            
        print(bcolors.RED + f"No product found with ID {user_change_product_id}")
        time.sleep(2)
    except ValueError:
        print(bcolors.RED + f"Product '{user_change_product}' does not exist, enter ID")
        time.sleep(2)
    return None        

# User input to inspect specific product
def inspect_products_dialog() -> Product:
    os.system("cls")
    print_products()
    user_change_product= input(bcolors.YELLOW + "What product would you like to inspect? (q to quit)")
    if user_change_product == "q":
        return None

    try:
        os.system("cls")
        user_change_product_id= int(user_change_product)
        for product in inventory.products:
            if user_change_product_id == product.id:
                seperator_top = "-" * 80
                seperator_bottom = "-" * 80
                print(bcolors.GREEN + f"CURRENTLY INSPECTING: {product.name}")
                print(bcolors.DEFAULT + seperator_top)
                print(bcolors.DEFAULT + f"Product Name: {product.name}\nProduct description: {product.desc}\nProduct price:{product.price}\nProduct_quantity:{product.quantity} ")
                print(bcolors.DEFAULT + seperator_bottom)
                input(bcolors.YELLOW + "Continue")

    except ValueError:
        print(bcolors.RED + f"Invalid input")
        time.sleep(2)
    return None        

# Show information about the csv file
def show_system_information():
    os.system("cls")
    seperator_top = "-" * 20
    seperator_bottom = "-" * 20
    total_product_quantity = []
    total_product_price = []
    total_product_types = len(inventory.products)

    for products in inventory.products:
        total_product_quantity.append(products.quantity)
        total_product_price.append(products.price)

    total_product_quantity = sum(total_product_quantity)
    total_product_price = round(sum(total_product_price))
    
    print(seperator_top)
    print(bcolors.YELLOW + f"Product_types: {total_product_types}\nTotal_product_quantity: {total_product_quantity}\nCombined_price: {total_product_price}kr")
    print(bcolors.DEFAULT + seperator_bottom)
    user_input = input("continue")
        

# Formating to swedish (like currency and time)
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

# Define filename
filename = 'db_products.csv'

# Create instance of inventory class initialzing with filename
inventory = Inventory(filename)

# Load the data from the CSV file to inventory object
inventory.load_data()

# Main program
while True:
    os.system('cls')
    print_products()
    try:
        User_Choice_Input = int(input(bcolors.DEFAULT + "1. Add Product\n2. Remove Product\n3. Change Product\n4. Inspect Product\n5. Show inventory information\n6. Exit\n"))
        if User_Choice_Input == 1:
            try:
                new_product = new_product_dialog()
                inventory.add(new_product)
            except ValueError:
                print(bcolors.RED + "Empty input")
                time.sleep(1.5)

        elif User_Choice_Input == 2:
            removed_product = remove_product_dialog()

        elif User_Choice_Input == 3:
            changed_product = change_product_dialog()
            if changed_product != None:
                print(f"ändrade {changed_product.name}")

        elif User_Choice_Input == 4:
            inspect_products_dialog()

        elif User_Choice_Input == 5:
            show_system_information()
        
        elif User_Choice_Input == 6:
            break
    except ValueError:
        print(bcolors.RED + "Wrong input, enter numbers 1-6")
        time.sleep(1.5)

print_products()
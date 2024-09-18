import csv
import os
import locale
import time

class Product:
    def __init__(self, id, name, desc, price, quantity) -> None:
        self.id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"Product: {self.name} \t {self.desc} \t {locale.currency(self.price, grouping=True)} \t {self.quantity}"

    
class Inventory:

    def __init__(self, filename:str) -> None:
        self.products = []
        self.filename = filename

    def add(self, product:Product) -> None:
        new_id = 1
        if len(self.products) > 0:
            new_id = max([product.id for product in self.products]) + 1 
        product.id = new_id
        self.products.append(product)

        # Append the new product to the CSV file
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product.id, product.name, product.desc, product.price, product.quantity])


    def load_data(self) -> None:
        self.products = []
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                desc = row['desc']
                price = float(row['price'])
                quantity = int(row['quantity'])
                
                self.products.append(Product(id, name, desc, price, quantity))


    def remove(self, id:int ) -> Product:
        removed_product:Product = None
        for i in range(len(self.products)) :
            prod = self.products[i]
            if prod.id == id:
                removed_product = self.products[id]
                del self.products[id]
                break
        
        # write products to the CSV file
        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ["id","name","desc","price","quantity"]
            # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for product in self.products:
                writer.writerow([product.id, product.name, product.desc, product.price, product.quantity])
        return removed_product



#User input for new product
def new_product_dialog() -> Product:
    name = input("Product_Name: ")
    desc = input("Product_Description: ")
    price = float(input("Product_Price: "))
    quantity = int(input("Product_Quantity: "))
    return Product(None, name, desc, price, quantity)


def remove_product_dialog() -> Product:
    print("\n".join([str(product.id) + ' ' + str(product) for product in inventory.products]))
    user_remove = int(input(f"What product would you like to remove?\n"))
    removed_product = inventory.remove(user_remove)
    return removed_product

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')


filename = 'db_products.csv'

inventory = Inventory(filename)
inventory.load_data()

#Main program
while True:
    os.system('cls')
    User_Choice_Input = int(input("1. Add Product\n2. Remove Product\n3. Change Product\n4. Exit\n"))
    if User_Choice_Input == 1:
        new_product = new_product_dialog()
        inventory.add(new_product)
    elif User_Choice_Input == 2:
        removed_product = remove_product_dialog()
        print(f"tog bort{removed_product.name}")

    elif User_Choice_Input == 3:
        while True:
            specific_user_choice_input_3 = input("1. Change_Name\n2. Change_Description\n3. Change_Price\nChoice: ")
            if specific_user_choice_input_3 == "1":
                user_choice_change_product_input1 = input("Change_Product: ")
                #Byta produkt namn
            elif specific_user_choice_input_3 == "2":
                user_choice_change_description_input_3 = input("Change_Description: ")
                # Här ska man lägga till byta namn
            elif specific_user_choice_input_3 == "3":
                user_choice_change_value_input_3 = int(input("New_Price: "))
                # Här ska man byta pris
    elif User_Choice_Input == 4:
        break

print(inventory.as_product_list())
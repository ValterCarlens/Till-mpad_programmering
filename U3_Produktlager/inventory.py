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

    def add_item(self, products, filename):
        new_id = max([product.id for product in products]) + 1 if products else 0
        name = input("Product_Name: ")
        desc = input("Product_Description: ")
        price = float(input("Product_Price: "))
        quantity = int(input("Product_Quantity: "))

        new_product = Product(new_id, name, desc, price, quantity)
        products.append(new_product)

        # Append the new product to the CSV file
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_product.id, new_product.name, new_product.desc, new_product.price, new_product.quantity])

    def __str__(self):
        return f"Product: {self.name} \t {self.desc} \t {locale.currency(self.price, grouping=True)}"

    


def load_data(filename):
    products = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(Product(id, name, desc, price, quantity))
    return products

def get_products(products):
    return "\n".join([str(product) for product in products])


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

os.system('cls')
filename = 'db_products.csv'
products = load_data(filename)

while True:
    User_Choice_Input = int(input("1. Add Product\n2. Remove Product\n3. Change Product\n4. Exit\n"))
    if User_Choice_Input == 1:
        new_product = Product(None, None, None, None, None)
        new_product.add_item(products, filename)
    elif User_Choice_Input == 2:
        print(get_products(products))
        user_remove = int(input(f"What product would you like to remove?\n1 - {len(products) + 1}\n"))
        products.remove(temp_product)
        return f"tog bort{temp_product["name"]}"

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

print(get_products(products))
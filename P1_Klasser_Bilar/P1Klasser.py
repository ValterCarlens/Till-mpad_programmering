import os

class Car:
    def __init__(self, make, model, color) -> None:
        self.make = make
        self.model = model
        self.color = color

    def view_car(self):
        return f"{self.make} - {self.model} ({self.color})"

os.system("cls")

cars = []
user_inputs=[1, 2]
user_car_choice_make = ""
user_car_choice_model = ""
user_car_choice_color = ""

while True:
    user_inputs=input("1, Add car 2,Remove Car: ")
    if user_inputs == "1":
        user_car_choice_make = input("BilMärke: ")
        user_car_choice_model = input("BilModel: ")
        user_car_choice_color = input("BilFärg: ")
        cars.append((Car(user_car_choice_make, user_car_choice_model, user_car_choice_color)))

    elif user_inputs == "2":
        user_remove_input=int(input(f"What car would you like to remove? 1 - {len(cars)}: "))
        cars.pop(user_remove_input - 1)
        


    for car in cars:
        print(f"{car.view_car()}")
import os
os.system("cls")

class Car:
    def __init__(self):
        self.car_details = []

    def add_car(self, make, model):
        self.car_details.append({"make": make, "model": model})

    def list_cars(self):
        for index, car in enumerate(self.car_details, start=1):
            print(f"{index}. {car['make']} - {car['model']}")

car = Car()

car.add_car("Volvo", "XC40")
car.add_car("Audi", "R8")
car.add_car("Volvo", "XC60")

car.list_cars()
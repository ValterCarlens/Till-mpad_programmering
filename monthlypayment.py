import os
os.system("cls")

def calculate_monthly_payment(principal, annual_rate, years):
    months=years*12
    annual_rate = annual_rate/100/12
    monthly_payment = (principal * annual_rate * (1+annual_rate)**months) / ((1 + annual_rate)**months - 1)
    return monthly_payment

principal = float(input("Lånebelopp: "))
annual_rate = float(input("Årsränta (%): "))
years = int(input("Löptid (år): "))
payment = calculate_monthly_payment(principal, annual_rate, years)
print(f"Din månatliga betalning är: {payment:.2f} kr")
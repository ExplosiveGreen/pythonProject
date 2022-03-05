import math


def main():
    current_salary = float(input("Enter your current salary: "))
    percent_raise = float(input("Enter the percent raise: "))
    current_savings = float(input("Enter the current savings: "))
    retierment_salery = float(input("Enter the retierment salary you want in bruto (25% tax): "))

    to_save = (retierment_salery*12*(1+percent_raise))/percent_raise - current_savings
    years = to_save/(current_salary*12*11)
    years = math.log(years + 1)/math.log(1.1)
    print("number of years",years)


if __name__ == "__main__":
    main()
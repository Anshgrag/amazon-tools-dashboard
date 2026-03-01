def add(a, b):
    return a + b

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

num1 = get_number("Enter first number: ")
num2 = get_number("Enter second number: ")

result = add(num1, num2)
print(f"Result: {result}")

# Python Calculator

# Add Operation
def add(x, y):
    return x + y

# Subtract Operation
def subtract(x, y):
    return x - y

# Multiply Operation
def multiply(x, y):
    return x * y

# Division Operation
def divide(x, y):
    return x / y

# Main Loop
while True:
    # Input Validation
    try:
        number1 = int(input("Enter first number: "))
        number2 = int(input("Enter second number: "))

        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        operation = int(input("Enter operation(1-5): "))
    except:
        print("Invalid input please try again")
        continue
    
    result = 0

    if operation == 1:
        result = add(number1, number2)
    elif operation == 2:
        result = subtract(number1, number2)
    elif operation == 3:
        result = multiply(number1, number2)
    elif operation == 4:
        result = divide(number1, number2)
    elif operation == 5:
        break
    else:
        print("Invalid operation")

    print("Result: ", result)
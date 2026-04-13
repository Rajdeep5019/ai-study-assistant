a = int(input("Enter the 1st number: "))
b = int(input("Enter the 2nd number: "))

choice = int(input("Choose operation: 1.Addition  2.Subtract  3.Multiply: "))

if choice == 1:
    print("Result:", a + b)
elif choice == 2:
    print("Result:", a - b)
elif choice == 3:
    print("Result:", a * b)
else:
    print("Invalid choice")
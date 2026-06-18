import random
import string
import hashlib

passwords = {}

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()" for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password():
    account = input("Enter Account Name: ")
    password = input("Enter Password: ")

    passwords[account] = hash_password(password)
    print("Password saved securely!")

def view_accounts():
    if not passwords:
        print("No accounts saved.")
        return

    print("\nStored Accounts")
    for account in passwords:
        print("-", account)

def analyze_password():
    password = input("Enter Password to Analyze: ")

    strength = check_strength(password)

    print("\nPassword Strength:", strength)

    if strength == "Weak":
        print("Suggestion:")
        print("- Use at least 12 characters")
        print("- Add uppercase letters")
        print("- Add numbers")
        print("- Add special characters")

def generate_new_password():
    length = int(input("Enter Password Length: "))
    password = generate_password(length)

    print("\nGenerated Password:")
    print(password)

def menu():
    while True:
        print("\n===== Secure Password Manager =====")
        print("1. Generate Password")
        print("2. Analyze Password Strength")
        print("3. Save Password")
        print("4. View Accounts")
        print("5. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            generate_new_password()

        elif choice == "2":
            analyze_password()

        elif choice == "3":
            save_password()

        elif choice == "4":
            view_accounts()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid Choice!")

menu()

import calculate_func
import user
import keyboard  # Import the keyboard module for custom password masking

# Encapsulated user credentials (avoid global variables)
CREDENTIALS = {
    "username": "OferShulami",
    "password": "12345678"  # Replace with a hashed password in real-world applications
}

def get_password(prompt='Password: '):
    """
    Function to hide password input with asterisks (*).
    """
    print(prompt, end='', flush=True)  # Print the prompt without newline
    password = ''
    
    while True:
        if keyboard.is_pressed('enter'):  # Enter key is pressed
            print()  # Move to the next line
            break
        elif keyboard.is_pressed('backspace'):  # Backspace key is pressed
            password = password[:-1]  # Remove last character
            print('\b \b', end='', flush=True)  # Erase the last asterisk
        else:
            # Get character typed and append to password
            char = keyboard.read_event(suppress=True).name
            if char != 'shift' and char != 'space':  # Ignore shift and space key itself
                password += char
                print('*', end='', flush=True)  # Display '*' as the user types
                
    return password


def validate_username(username: str) -> bool:
    """
    Validate the provided username.
    """
    return username == CREDENTIALS["username"]


def validate_password(password: str) -> bool:
    """
    Validate the provided password.
    """
    return password == CREDENTIALS["password"]


def login() -> bool:
    """
    Handle the login process, allowing retries for invalid inputs.
    """
    while True:
        username = input("Please enter username: ")
        password = get_password("Please enter password: ")  # Custom password input with masking
        if validate_username(username) and validate_password(password):
            print("Login successful")
            return True
        elif validate_username(username):
            print("Invalid password\nPlease try again.")
        elif validate_password(password):
            print("Invalid username\nPlease try again.")
        else:
            print("Invalid username and password\nPlease try again.")


def main():
    """
    Main function to handle the program flow.
    """
    log = 0
    ofer = None  # Initialize the account object here

    while True:
        # Check if the user is logged in
        if log == 0:
            if login():
                ofer = user.Account(CREDENTIALS["username"], CREDENTIALS["password"])  # Create account object
                log = 1  # Set login status to 1 after successful login

        if log == 1:  # Once logged in, show options
            print("\nSelect your option:")
            print("a - For buy or sell")
            print("s - For show account details")
            print("q - For logout")

            option = input("Choose an option: ")

            if option == "a":
                a = 0
                while a == 0:
                    answer = input("for buy select b and for sell select s\nto go back press q")

                    if answer == "b":
                        a = 1
                        ticker = input("tiker: ")
                        amount = int(input("amount: "))
                        price = float(input("price per stock: "))
                        date = input("the date in YYYY-MM-DD format: ")
                    elif answer == "s":
                        a = 1
                        print("not avalible yet")
                    elif answer == "q":
                        a = 1
                        print("returning to the menu")

                    else:
                        print("Invalid\nplease try again")

            elif option == "s":
                # Show account details
                print(f"Account details for {ofer.name}:")
                # Add account details logic here, e.g., display stock holdings, portfolio status, etc.
            elif option == "q":
                print("Logging out...")
                log = 0  # Reset login status to log out
                ofer = None  # Clear the account object
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

import calculate_func
import user
import getpass

global USERNAME
global PASSWORD

def login() -> bool:

    global USERNAME
    global PASSWORD 

    while True:
        username = input("enter username: ")
        password = input_password()
        if username == USERNAME and password == PASSWORD:
            return True
        elif username != USERNAME and password == PASSWORD:
            print("your username isn't correct\nplease try again")
        elif username == USERNAME and password != PASSWORD:
            print("your password isn't correct\nplease try again")
            if try_again_password(USERNAME):
                return True
        else: 
            print("your username and password isn't correct\nplease try again")


def try_again_password(correct_username) -> bool:
    global PASSWORD
    print(f"username: {correct_username}")
    password = input_password()
    if password == PASSWORD:
        return True
    else: 
        print("your password isn;t correct\nplease try again")
        return False

def input_password() -> str:

    password = getpass.getpass("Enter your password: ")
    return password

def print_menu_and_input_option() -> str:

    print("\nSelect your option:")
    print("a - For buy or sell")
    print("s - For show account details")
    print("q - For logout")

    option = input("Choose an option: ")

    return option

def main():
    
    
    global USERNAME
    global PASSWORD

    USERNAME = "OferShulami"
    PASSWORD = "12345678"
    log = 0
    ofer = None  # Initialize the account object here

    while True:
        # Check if the user is logged in
        if log == 0:
            if login():
                ofer = user.Account(USERNAME, PASSWORD)  # Create account object
                log = 1  # Set login status to 1 after successful login

        if log == 1:  # Once logged in, show options

            option = print_menu_and_input_option()

            if option == "a":
                # Implement buy or sell logic
                print("Buy or Sell functionality (not implemented yet)")
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

import calculate_func
import user  # ודא שהקובץ user.py נמצא באותה תיקייה
import getpass

# נתוני גישה מוגדרים מראש
CREDENTIALS = {
    "username": "OferShulami",
    "password": "1"  # שנה לסיסמה שלך
}


def login() -> bool:
    """ניהול תהליך ההתחברות למערכת"""
    print(f"\n{'=' * 35}")
    print("      WELCOME TO MONEYER")
    print(f"{'=' * 35}")

    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        if username == CREDENTIALS["username"] and password == CREDENTIALS["password"]:
            print("\n[V] Login Successful!")
            return True
        else:
            print("[X] Invalid credentials. Please try again.\n")


def print_menu() -> str:
    """הצגת תפריט האפשרויות הראשי"""
    print(f"\n{'-' * 35}")
    print("MAIN MENU:")
    print("a - Buy or Sell Stocks")
    print("s - Show Portfolio Status")
    print("p - Show Profit Report")
    print("q - Logout & Exit")
    return input("\nChoose an option: ").lower()


def main():
    # אתחול הגדרות Pandas לתצוגה יפה בטרמינל
    calculate_func.setup_pd()

    is_logged_in = False
    ofer_account = None

    while True:
        # שלב 1: התחברות
        if not is_logged_in:
            if login():
                # יצירת אובייקט החשבון
                ofer_account = user.Account(CREDENTIALS["username"], CREDENTIALS["password"])
                is_logged_in = True
            else:
                continue

        # שלב 2: תפריט פעולות
        option = print_menu()

        if option == "a":
            # תפריט קנייה/מכירה
            action = input("\n[b] Buy | [s] Sell | [q] Back: ").lower()

            if action == "q":
                continue

            try:
                ticker = input("Ticker (e.g., AAPL): ").upper()
                amount = int(input("Amount of shares: "))

                # בחירה בין הזנה ידנית למשיכה אוטומטית
                print("\nWould you like to enter price/date manually?")
                print("(If 'n', system will fetch current market price automatically)")
                choice = input("Manual entry? (y/n): ").lower()

                price = None
                date = None

                if choice == 'y':
                    price = float(input("Enter Price: "))
                    date = input("Enter Date (YYYY-MM-DD): ")

                if action == "b":
                    print(f"[*] Processing Buy for {ticker}...")
                    ofer_account.buy_stock(ticker, amount, price, date)
                    print("[V] Transaction Successful.")

                elif action == "s":
                    print(f"[*] Processing Sell for {ticker}...")
                    ofer_account.sell_stock(ticker, amount, price, date)
                    print("[V] Transaction Successful.")

            except ValueError as e:
                print(f"\n[!] Input Error: {e}")
            except Exception as e:
                print(f"\n[!] Error: {e}")

        elif option == "s":
            print(f"\n{'*' * 10} Current Portfolio {'*' * 10}")
            ofer_account.show_account_info()

        elif option == "p":
            start_d = input("Enter start date (YYYY-MM-DD) or press Enter for 'all time': ")
            if not start_d:
                # מציג רווח מתחילת הפעילות
                ofer_account.show_profit()
            else:
                # מציג רווח מתאריך ספציפי ועד היום
                ofer_account.show_profit(start_date=start_d)

        elif option == "q":
            print("\nLogging out... See you next time!")
            is_logged_in = False
            ofer_account = None
            break

        else:
            print("\n[!] Invalid option. Please try again.")


if __name__ == "__main__":
    main()
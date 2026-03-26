import calculate_func
from colorama import Fore, Style, init
from tabulate import tabulate

# אתחול הצבעים
init(autoreset=True)

class Account:
    """
    Represents an account for managing stock trades, including buying, selling, and portfolio tracking.

    Attributes:
        __type__ (str): Identifies the class as "Account".
        name (str): The name of the account holder.
        password (str): The password for the account.
        tickers_buy_dict (dict): A dictionary containing details about purchased tickers.
            Structure:
                {
                    ticker (str): {
                        "num" (list[int]): List of trade numbers.
                        "amount" (list[int]): List of amounts bought.
                        "price" (list[float]): List of prices per share.
                        "date" (list[str]): List of purchase dates.
                    }
                }
        tickers_sell_dict (dict): A dictionary containing details about sold tickers.
            Structure:
                {
                    ticker (str): {
                        "num" (list[int]): List of trade numbers.
                        "amount" (list[int]): List of amounts sold.
                        "price" (list[float]): List of prices per share.
                        "date" (list[str]): List of sale dates.
                    }
                }
        account_dict (dict): A dictionary tracking the account's portfolio details.
            Structure:
                {
                    ticker (str): {
                        "amount" (int): Total amount of stock held.
                        "initial price" (float): Initial purchase price per share.
                        "current price" (float): Current market price per share.
                        "stock value in Portfolio" (float): Current value of the stock in the portfolio.
                        "Price Change" (float): Difference between current and initial stock value.
                        "percentage change" (float): Percentage change in stock value from initial price.
                        "percentage portfolio" (float): Percentage of the portfolio's total value represented by this stock.
                    }
                }
        profit_dict (dict): A dictionary tracking profit and historical performance metrics.
            Structure:
                {
                    ticker (str): {
                        "initial amount" (int): The amount of stock held at the start date.
                        "final amount" (int): The amount of stock held at the end date.
                        "initial price" (float): The stock price at the start date.
                        "final price" (float): The stock price at the end date.
                        "initial stock value in Portfolio" (float): Value of the stock at the start date.
                        "final stock value in Portfolio" (float): Value of the stock at the end date.
                        "profit" (float): The calculated profit or loss.
                        "percentage change" (float): Percentage change in stock value in the given timeframe.
                        "percentage in portfolio" (float): Percentage of the portfolio's total value.
                    }
                }
    """

    def __init__(self, name: str, password: str) -> None:
        """
        Initializes an Account object.

        Args:
            name (str): The name of the account holder.
            password (str): The password for the account.
        """
        self.__type__ = "Account"
        self.name = name
        self.password = password

        self.tickers_buy_dict = {}
        self.tickers_sell_dict = {}
        self.account_dict = {}
        self.profit_dict = {}

    def __repr__(self) -> str:
        """
        Returns a string representation of the Account object.

        Returns:
            str: A string displaying the account name and type.
        """
        return f"Account(name={self.name}, __type__={self.__type__})"

    def buy_stock(self, ticker: str, amount: int, price_per_stock: float = None, date: str = "Error") -> None:
        """
        Adds purchase details to the account for a specific stock.

        Updates the tickers_buy_dict and account_dict with the provided details about a stock purchase.

        Args:
            ticker (str): The stock ticker symbol (e.g., "AAPL").
            amount (int): The number of stocks purchased.
            price_per_stock (float, optional): The purchase price per stock.
            date (str, optional): The date of purchase in the format 'YYYY-MM-DD'.

        Raises:
            ValueError: If both price_per_stock and date are missing, or if the ticker/date is invalid.
        """
        ticker = ticker.upper()

        # Check if there is enough data
        if price_per_stock is None and date is None:
            raise ValueError("You are missing the date or price.")

        # Check if ticker is valid
        if not calculate_func.is_valid_ticker(ticker):
            raise ValueError(f"This ticker {ticker} is invalid.")

        date = calculate_func.check_date(date)

        if ticker not in self.tickers_buy_dict:
            self.tickers_buy_dict[ticker] = {
                "num": [],
                "amount": [],
                "price": [],
                "date": []
            }

        # Update the ticker buy dict
        calculate_func.super_update(self.tickers_buy_dict, ticker, amount, price_per_stock, date)

        # Update the account dict
        self.account_dict = calculate_func.update_account_dict(
            True, ticker, self.account_dict, self.tickers_sell_dict, self.tickers_buy_dict
        )

    def sell_stock(self, ticker: str, amount: int, price_per_stock: float = None, date: str = None) -> None:
        """
        Records the sale of a stock by adding the provided details to the tickers_sell_dict.

        Args:
            ticker (str): The stock ticker symbol.
            amount (int): The number of shares sold.
            price_per_stock (float, optional): The price at which each stock was sold.
            date (str, optional): The date of the sale in the format 'YYYY-MM-DD'.

        Raises:
            ValueError: If the stock ticker is not found in the user's account.
            ValueError: If trying to sell more stocks than owned.
            ValueError: If both price_per_stock and date are not provided.
        """
        ticker = ticker.upper()

        if ticker not in self.tickers_buy_dict:
            raise ValueError(f"You don't have this ticker in your account: {ticker}")

        date = calculate_func.check_date(date)

        if ticker not in self.tickers_sell_dict:
            self.tickers_sell_dict[ticker] = {
                "num": [],
                "amount": [],
                "price": [],
                "date": []
            }

        # Check if selling more than owned
        if amount > self.account_dict[ticker]["amount"]:
            raise ValueError(
                f"You want to sell {amount} stocks but you have only {self.account_dict[ticker]['amount']} stocks.")

        if price_per_stock is None and date is None:
            raise ValueError("You are missing the date or price.")

        calculate_func.super_update(self.tickers_sell_dict, ticker, amount, price_per_stock, date)

        # Update the account dict
        self.account_dict = calculate_func.update_account_dict(
            False, ticker, self.account_dict, self.tickers_sell_dict, self.tickers_buy_dict
        )

    def show_buy_info(self) -> None:
        """Displays detailed buy order information."""
        calculate_func.show_order_info(self.tickers_buy_dict, order="buy")

    def show_sell_info(self) -> None:
        """Displays detailed sell order information."""
        calculate_func.show_order_info(self.tickers_sell_dict, order="sell")

    def show_account_info(self):
        """מציגה את תיק ההשקעות בפורמט מקצועי וצבעוני לטרמינל"""
        if not self.account_dict:
            print("\n[!] Portfolio is empty.")
            return

        table_data = []

        for ticker, info in self.account_dict.items():
            # שימוש ב-.get() מאפשר לנו למשוך נתונים בלי שהקוד יקרוס אם השם מעט שונה
            amount = info.get('amount', 0)
            init_price = info.get('initial price', 0)
            curr_price = info.get('current price', 0)

            # כאן היה ה-KeyError: שינינו ל-lowercase 'price change'
            price_change = info.get('price change', 0)
            change_pct = info.get('percentage change', 0)
            weight = info.get('percentage portfolio', 0)

            # בחירת צבע: ירוק לרווח, אדום להפסד
            color = Fore.GREEN if change_pct >= 0 else Fore.RED
            reset = Style.RESET_ALL
            sign = "+" if change_pct >= 0 else ""

            row = [
                ticker.upper(),
                f"{amount}",
                f"${init_price:,.2f}",
                f"${curr_price:,.2f}",
                f"{color}{sign}{price_change:,.2f}{reset}",
                f"{color}{sign}{change_pct:.2f}%{reset}",
                f"{weight:.1f}%"
            ]
            table_data.append(row)

        headers = [
            "Ticker", "Shares", "Avg. Cost",
            "Market Price", "Gain/Loss ($)", "Change (%)", "Weight"
        ]

        print(f"\n{'=' * 20} PORTFOLIO SUMMARY {'=' * 20}")
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign="center"))
        print(f"{'=' * 61}\n")

    def show_profit(self, ticker: str = "all", start_date: str = "first buy time", end_date: str = "now") -> None:
        """
        Calculates and displays the profit/loss for a specific ticker or the entire portfolio.

        Args:
            ticker (str, optional): The stock ticker, or "all" for the whole portfolio. Defaults to "all".
            start_date (str, optional): The starting date for calculation. Defaults to "first buy time".
            end_date (str, optional): The ending date for calculation. Defaults to "now".
        """
        ticker = ticker.upper()
        self.profit_dict = {}

        start_date, end_date = calculate_func.sub_date(start_date, end_date)

        if ticker == "ALL":
            for t in self.tickers_buy_dict:
                self.profit_dict = calculate_func.profit(
                    t, start_date, end_date, self.tickers_buy_dict,
                    self.tickers_sell_dict, self.account_dict, self.profit_dict
                )
        else:
            calculate_func.profit(
                ticker, start_date, end_date, self.tickers_buy_dict,
                self.tickers_sell_dict, self.account_dict, self.profit_dict
            )

        self.profit_dict = calculate_func.create_all_profit_dict(self.profit_dict)
        calculate_func.make_account_table(self.profit_dict)

def main():
    calculate_func.setup_pd()

    # לוגו פתיחה מרשים
    logo = """
    ███╗   ███╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗███████╗██████╗ 
    ████╗ ████║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗
    ██╔████╔██║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ █████╗  ██████╔╝
    ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  ██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗   ██║   ███████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    """
    print(logo)
    print(f"{' ':<10}--- PORTFOLIO MANAGEMENT SYSTEM ---")
    print(f"{'=' * 65}\n")

    ofer = Account("Ofer", "1234")

    # הרצת פקודות
    print(f"[*] Connecting to Yahoo Finance...")
    print(f"[*] Loading assets for {ofer.name}...")

    ofer.buy_stock("AAPL", 10, date="2026-03-25")
    ofer.buy_stock("GOOGL", 10, date="2026-03-25")
    ofer.buy_stock("META", 10, date="2026-03-25")
    ofer.buy_stock("NVDA", 10, date="2026-03-25")
    ofer.buy_stock("MSFT", 10, date="2026-03-25")

    print(f"\n{'-' * 20} PORTFOLIO SUMMARY {'-' * 20}")
    ofer.show_account_info()
    print(f"{'=' * 65}\n")

if __name__ == '__main__':
    main()

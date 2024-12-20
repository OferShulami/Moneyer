import calculate_func


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
                        "Percentage Change" (float): Percentage change in stock value from initial price.
                        "percentage portfolio" (float): Percentage of the portfolio's total value represented by this stock.
                    }
                }

    Methods:
        __init__(name: str, password: str):
            Initializes the Account with the given name, password, and empty dictionaries for tracking trades and portfolio details.
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



    def __repr__(self):
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
            price_per_stock (float, optional): The purchase price per stock. Must not be None.
            date (str, optional): The date of purchase in the format 'YYYY-MM-DD'. Must not be None.

        Raises:
            ValueError: If either price_per_stock or date is missing, or if the ticker or date is invalid.
        """
        ticker = ticker.upper()

        # Check if there is enough data
        if price_per_stock is None and date is None:
            raise ValueError(f"You are missing the date or price.")

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
        self.account_dict = calculate_func.update_account_dict(True, ticker, self.account_dict, self.tickers_sell_dict,
                                                               self.tickers_buy_dict)


    def sell_stock(self, ticker: str, amount: int, price_per_stock: float = None, date: str = None) -> None:
        """
        Records the sale of a stock by adding the provided details to the `tickers_sell_dict`.

        This method validates that the stock (ticker) exists in the user's account (`tickers_buy_dict`). 
        If the ticker is not already present in `tickers_sell_dict`, it initializes an entry for it.

        Args:
            ticker (str): The stock ticker symbol.
            amount (int): The number of shares sold.
            price_per_stock (float, optional): The price at which each stock was sold. Defaults to None.
            date (str, optional): The date of the sale in the format 'YYYY-MM-DD'. Defaults to None.

        Raises:
            ValueError: If the stock ticker is not found in the user's account.
            ValueError: If both `price_per_stock` and `date` are not provided.

        Updates:
            - `tickers_sell_dict`: Adds the sale details including the number of shares sold, 
            the price per stock, and the sale date.

        Example:
            self.sell_stock('AAPL', 10, 150.0, '2024-12-01')
            This adds the sale information for the 'AAPL' ticker to `tickers_sell_dict`.
        """

        ticker = ticker.upper()

    
        if ticker not in self.tickers_buy_dict:
            raise ValueError(f"You don't have this ticker in your account: {ticker}")

        if ticker not in self.tickers_sell_dict:
            self.tickers_sell_dict[ticker] = {
                "num": [],
                "amount": [],
                "price": [],
                "date": []
            }
        else:
            if amount > self.account_dict[ticker]["amount"]:
                raise ValueError(f"You want to sell {amount} stocks but you have only {self.account_dict[ticker]['amount']} stocks")
            
        if price_per_stock is None and date is None:
            raise ValueError("You are missing the date or price.")
        
    

        calculate_func.super_update(self.tickers_sell_dict, ticker, amount, price_per_stock, date)
        # Update the account dict
        self.account_dict = calculate_func.update_account_dict(False, ticker, self.account_dict, self.tickers_sell_dict,
                                                               self.tickers_buy_dict)

    def show_buy_info(self):
        calculate_func.show_order_info(self.tickers_buy_dict, order="buy")

    def show_sell_info(self):
        calculate_func.show_order_info(self.tickers_sell_dict, order="sell")

    def show_account_info(self):
        calculate_func.create_account_sum(self.account_dict)
        calculate_func.make_account_table(self.account_dict)
    
    def show_profit(self,ticker: str = "all", start_date: str = "first buy time", end_date: str = "now"):
        calculate_func.profit(ticker, start_date, end_date, self.tickers_buy_dict, self.tickers_sell_dict, self.account_dict)



def main():
    
    calculate_func.setup_pd()
    ofer = Account("guy", "1234")
    ofer.buy_stock("voo", 1, price_per_stock=100, date="2012-4-04")
    ofer.buy_stock("voo", 10, price_per_stock=100, date="2014-11-11")
    ofer.buy_stock("voo", 10, price_per_stock=100, date="2014-11-12")

    ofer.sell_stock("voo", 1, price_per_stock=100, date="2000-9-11")
    ofer.sell_stock("voo", 1, price_per_stock=100, date="2023-9-11")
    ofer.sell_stock("voo", 1, price_per_stock=100, date="2024-9-11")




    
    #ofer.show_buy_info()
    # ofer.show_sell_info()
    #ofer.show_account_info()
    ofer.show_profit("voo", "2024-1-1", "2024-12-10")


if __name__ == '__main__':
    main()

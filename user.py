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
        profit_dict (dict): .
            Structure:
                {
                    ticker (str): {
                        "initial amount" (int): 
                        "final amount" (int): 
                        "initial price" (float):
                        "final price" (float): 
                        "initial stock value in Portfolio" (float): 
                        "final stock value in Portfolio" (float): Current value of the stock in the portfolio.
                        "profit" (float): Difference between current and initial stock value.
                        "Percentage Change" (float): Percentage change in stock value from initial price.
                        "percentage in portfolio" (float): Percentage of the portfolio's total value represented by this stock.
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
        self.profit_dict = {}

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
        #self.account_dict = calculate_func.check_and_update_for_splits()
        # Update the ticker buy dict
        self.tickers_buy_dict = calculate_func.super_update(self.tickers_buy_dict, ticker, amount, price_per_stock, date)
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

        date = calculate_func.check_date(date)

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
        
    

        self.tickers_sell_dict = calculate_func.super_update(self.tickers_sell_dict, ticker, amount, price_per_stock, date)
        # Update the account dict
        self.account_dict = calculate_func.update_account_dict(False, ticker, self.account_dict, self.tickers_sell_dict,
                                                               self.tickers_buy_dict)

    def show_buy_info(self):
        calculate_func.show_order_info(self.tickers_buy_dict, order="buy")

    def show_sell_info(self):
        calculate_func.show_order_info(self.tickers_sell_dict, order="sell")

    def show_account_info(self):
        self.account_dict = calculate_func.create_account_sum(self.account_dict)
        calculate_func.make_account_table(self.account_dict)
    
    def show_profit(self, ticker: str = "all", start_date: str = "first buy time", end_date: str = "now"):
        ticker = ticker.upper()
        self.profit_dict = {}
        start_date, end_date = calculate_func.sub_date(start_date, end_date)

        if ticker == "ALL":
            for ticker in self.tickers_buy_dict:
                self.profit_dict = calculate_func.profit(ticker, start_date, end_date, self.tickers_buy_dict, self.tickers_sell_dict, self.account_dict, self.profit_dict)

        else:
            calculate_func.profit(ticker, start_date, end_date, self.tickers_buy_dict, self.tickers_sell_dict, self.account_dict, self.profit_dict)


        self.profit_dict = calculate_func.create_all_profit_dict(self.profit_dict)
        
        calculate_func.make_account_table(self.profit_dict)

def main():
    
    calculate_func.setup_pd()
    ofer = Account("guy", "1234")

    # 2021
    # ofer.buy_stock("crsr", 17, date="2021-12-01")
    # ofer.buy_stock("ual", 3, date="2021-12-01")
    # ofer.buy_stock("abnb", 2, date="2021-12-01")
    # ofer.buy_stock("meta", 1, date="2021-12-01")
    # ofer.buy_stock("tsla", 1, date="2021-12-01") ###tsla split
    # ofer.buy_stock("msft", 1, date="2021-12-01")
    # ofer.buy_stock("aapl", 2, date="2021-12-01")
    # ofer.buy_stock("voo", 4, date="2021-12-01")

    # #2022
    # #feb
    # ofer.buy_stock("xle", 3, date="2022-02-04")
    # ofer.buy_stock("bito", 12, date="2022-02-04")
    # ofer.buy_stock("xle", 4, date="2022-02-04")
    # ofer.buy_stock("meta", 1, date="2022-02-04")
    # ofer.buy_stock("voo", 2, date="2022-02-04")
    # ofer.sell_stock("ual", 3, date="2022-02-24")
    # ofer.sell_stock("aapl", 2, date="2022-02-24")
    # ofer.sell_stock("bito", 12, date="2022-02-24")
    # ofer.sell_stock("voo", 6, date="2022-02-24")
    # #march
    # ofer.buy_stock("voo", 5, date="2022-03-16")
    # ofer.buy_stock("bito", 13, date="2022-03-16")
    # ofer.buy_stock("ual", 4, date="2022-03-16")
    # ofer.buy_stock("aapl", 2, date="2022-03-16")
    # #april
    # ofer.buy_stock("aapl", 4, date="2022-04-18")
    # ofer.buy_stock("bito", 24, date="2022-04-18")
    # ofer.buy_stock("meta", 1, date="2022-04-18")
    # ofer.buy_stock("aapl", 1, date="2022-04-18")
    # ofer.buy_stock("voo", 4, date="2022-04-18")
    # #june
    # ofer.sell_stock("xle", 7, date="2022-06-10")
    # ofer.buy_stock("qqq", 6, date="2022-06-10")
    # ofer.buy_stock("smh", 7, date="2022-06-10")
    # ofer.buy_stock("tsm", 2, date="2022-06-10")
    # ofer.buy_stock("intc", 8, date="2022-06-10")
    # ofer.buy_stock("amd", 2, date="2022-06-10")
    # ofer.buy_stock("nvda", 2, date="2022-06-10")
    # ofer.buy_stock("voo", 5, date="2022-06-10")
    # ofer.buy_stock("aapl", 2, date="2022-06-10")
    # ofer.buy_stock("msft", 1, date="2022-06-10")
    # ofer.buy_stock("ual", 8, date="2022-06-10")
    # ofer.buy_stock("meta", 1, date="2022-06-10")
    # ofer.buy_stock("qqq", 1, date="2022-06-10")
    # ofer.buy_stock("alb", 1, date="2022-06-22")
    # #jule
    # ofer.buy_stock("ual", 6, date="2022-07-13")
    # #agust
    # ofer.sell_stock("alb", 1, date="2022-08-02")
    # ofer.sell_stock("tsm", 2, date="2022-08-19")
    # ofer.buy_stock("ual", 21, date="2022-08-22")
    # ofer.buy_stock("msft", 14, date="2022-08-22")
    # ofer.buy_stock("aal", 57, date="2022-08-22")
    # ofer.buy_stock("ual", 21, date="2022-08-22")
    # ofer.buy_stock("intc", 57, date="2022-08-22")
    # ofer.buy_stock("smh", 9, date="2022-08-22")
    # ofer.buy_stock("tsla", 2, date="2022-08-22") ### check split
    # ofer.buy_stock("nvda", 17, date="2022-08-22")
    # ofer.buy_stock("qqq", 32, date="2022-08-22")
    # ofer.buy_stock("voo", 13, date="2022-08-22")
    # ofer.buy_stock("aapl", 31, date="2022-08-29")
    # ofer.buy_stock("googl", 55, date="2022-08-29")
    # #dec
    # ofer.sell_stock("crsr", 17, date="2022-12-07")
    # ofer.sell_stock("abnb", 2, date="2022-12-07")
    # #2023
    # #feb
    # ofer.buy_stock("aal", 109, date="2023-02-24")
    # ofer.buy_stock("ual", 13, date="2023-02-24")
    # ofer.buy_stock("bito", 321, date="2023-02-24")
    # ofer.buy_stock("tsla", 44, date="2023-02-24")
    # ofer.buy_stock("amd", 31, date="2023-02-24")
    # ofer.buy_stock("intc", 38, date="2023-02-24")
    # ofer.buy_stock("nvda", 10, date="2023-02-24")
    # ofer.buy_stock("smh", 13, date="2023-02-24")
    # ofer.buy_stock("meta", 36, date="2023-02-24")
    # ofer.buy_stock("googl", 156, date="2023-02-24")
    # ofer.buy_stock("aapl", 88, date="2023-02-24")
    # ofer.buy_stock("msft", 60, date="2023-02-24")
    # ofer.buy_stock("qqq", 61, date="2023-02-24")
    # ofer.buy_stock("voo", 82, date="2023-02-24")
    # #aug
    # ofer.buy_stock("smh", 14, date="2023-08-14")
    # ofer.buy_stock("aapl", 6, date="2023-08-14")
    # ofer.buy_stock("meta", 39, date="2023-08-14")
    # ofer.buy_stock("intc", 11, date="2023-08-14")
    # ofer.buy_stock("googl", 14, date="2023-08-14")
    # ofer.buy_stock("tsla", 3, date="2023-08-14")
    # ofer.buy_stock("amd", 4, date="2023-08-14")
    # ofer.buy_stock("msft", 7, date="2023-08-14")
    # ofer.buy_stock("bito", 43, date="2023-08-14")
    # ofer.buy_stock("qqq", 45, date="2023-08-14")
    # ofer.buy_stock("voo", 20, date="2023-08-14")
    # #oc
    # ofer.sell_stock("qqq", 64, date="2023-10-30")   ##################
    # ofer.buy_stock("voo", 30, date="2023-10-30")
    # #2024
    # #may
    # ofer.buy_stock("voo", 67, date="2024-05-01")
    # ofer.buy_stock("qqq", 81, date="2024-05-01")
    # #july
    # ofer.buy_stock("voo", 36, date="2024-07-05")
    # ofer.buy_stock("qqq", 41, date="2024-07-05")
    # ofer.buy_stock("voo", 3, date="2024-07-24")
    # ofer.buy_stock("qqq", 6, date="2024-07-24")
    # ofer.buy_stock("smh", 8, date="2024-07-24")
    # #sep
    # ofer.buy_stock("voo", 12, date="2024-09-23")
    # #nov
    # ofer.buy_stock("qqq", 15, date="2024-11-12")
    # #dec
    # ofer.buy_stock("qqq", 5, date="2024-09-12")
    # ofer.buy_stock("bito", 10, date="2024-09-12")
    # ofer.buy_stock("nvda", 1, date="2024-09-12")
    # ofer.buy_stock("qqq", 9, date="2024-12-18")
    # ofer.buy_stock("voo", 4, date="2024-12-18")
    # ofer.buy_stock("meta", 3, date="2024-12-18")
    # ofer.buy_stock("googl", 9, date="2024-12-18")
    # ofer.buy_stock("msft", 4, date="2024-12-18")
    # ofer.buy_stock("aapl", 7, date="2024-12-18")
    
    
    # print(ofer.tickers_buy_dict, "\n\n")
    # print(ofer.tickers_sell_dict, "\n\n")
    # print(ofer.account_dict, "\n\n")
        
    #check: TSLA, SMH. BITO. NVDA, UAL

    ofer.tickers_buy_dict = {
    'AAL': {'num': [1, 2], 'amount': [57, 109], 'price': [13.710000038146973, 15.5600004196167], 'date': ['2022-08-22', '2023-02-24']},
    'AAPL': {'num': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'amount': [2, 2, 4, 1, 2, 31, 88, 6, 7], 'price': [162.1144561767578, 157.21795654296875, 162.6165313720703, 162.6165313720703, 135.29029846191406, 159.43612670898438, 145.40496826171875, 178.3501434326172, 248.0500030517578], 'date': ['2021-12-01', '2022-03-16', '2022-04-18', '2022-04-18', '2022-06-10', '2022-08-29', '2023-02-24', '2023-08-14', '2024-12-18']},
    'ABNB': {'num': [1], 'amount': [2], 'price': [163.0800018310547], 'date': ['2021-12-01']},
    'ALB': {'num': [1], 'amount': [1], 'price': [210.49078369140625], 'date': ['2022-06-22']},
    'AMD': {'num': [1, 2, 3], 'amount': [2, 31, 4], 'price': [94.81999969482422, 78.08999633789062, 111.9800033569336], 'date': ['2022-06-10', '2023-02-24', '2023-08-14']},
    'BITO': {'num': [1, 2, 3, 4, 5, 6], 'amount': [12, 13, 24, 321, 43, 10], 'price': [11.50643253326416, 11.551447868347168, 11.429899215698242, 6.558293342590332, 8.020268440246582, 14.56792163848877], 'date': ['2022-02-04', '2022-03-16', '2022-04-18', '2023-02-24', '2023-08-14', '2024-09-12']},
    'CRSR': {'num': [1], 'amount': [17], 'price': [21.34000015258789], 'date': ['2021-12-01']},
    'GOOGL': {'num': [1, 2, 3, 4], 'amount': [55, 156, 14, 9], 'price': [109.0247802734375, 88.80806732177734, 130.8556365966797, 188.39999389648438], 'date': ['2022-08-29', '2023-02-24', '2023-08-14', '2024-12-18']},
    'INTC': {'num': [1, 2, 3, 4], 'amount': [8, 57, 38, 11], 'price': [36.90437316894531, 32.196311950683594, 24.537330627441406, 35.09306335449219], 'date': ['2022-06-10', '2022-08-22', '2023-02-24', '2023-08-14']},
    'META': {'num': [1, 2, 3, 4, 5, 6, 7], 'amount': [1, 1, 1, 1, 36, 39, 3], 'price': [309.4180603027344, 236.18777465820312, 209.9679412841797, 174.90188598632812, 169.74160766601562, 305.02484130859375, 597.1900024414062], 'date': ['2021-12-01', '2022-02-04', '2022-04-18', '2022-06-10', '2023-02-24', '2023-08-14', '2024-12-18']},
    'MSFT': {'num': [1, 2, 3, 4, 5, 6], 'amount': [1, 1, 14, 60, 7, 4], 'price': [321.73577880859375, 247.67999267578125, 272.4974365234375, 245.81021118164062, 320.3052062988281, 437.3900146484375], 'date': ['2021-12-01', '2022-06-10', '2022-08-22', '2023-02-24', '2023-08-14', '2024-12-18']},
    'NVDA': {'num': [1, 2, 3, 4], 'amount': [2, 17, 10, 1], 'price': [16.952287673950195, 17.012210845947266, 23.269075393676758, 119.13179016113281], 'date': ['2022-06-10', '2022-08-22', '2023-02-24', '2024-09-12']},
    'QQQ': {'num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'amount': [6, 1, 32, 61, 45, 81, 41, 6, 15, 5, 9], 'price': [283.42718505859375, 283.42718505859375, 309.06195068359375, 288.13507080078125, 366.70428466796875, 419.5838928222656, 494.66607666015625, 461.98480224609375, 512.084228515625, 471.795166015625, 515.6384887695312], 'date': ['2022-06-10', '2022-06-10', '2022-08-22', '2023-02-24', '2023-08-14', '2024-05-01', '2024-07-05', '2024-07-24', '2024-11-12', '2024-09-12', '2024-12-18']},
    'SMH': {'num': [1, 2, 3, 4, 5], 'amount': [7, 9, 13, 14, 8], 'price': [109.50363159179688, 110.96159362792969, 117.86895751953125, 149.09649658203125, 239.91664123535156], 'date': ['2022-06-10', '2022-08-22', '2023-02-24', '2023-08-14', '2024-07-24']},
    'TSLA': {'num': [1, 2, 3, 4], 'amount': [1, 2, 44, 3], 'price': [365.0, 289.913330078125, 196.8800048828125, 239.75999450683594], 'date': ['2021-12-01', '2022-08-22', '2023-02-24', '2023-08-14']},
    'TSM': {'num': [1], 'amount': [2], 'price': [84.36747741699219], 'date': ['2022-06-10']},
    'UAL': {'num': [1, 2, 3, 4, 5, 6, 7], 'amount': [3, 4, 8, 6, 21, 21, 13], 'price': [39.060001373291016, 41.189998626708984, 41.15999984741211, 37.90999984741211, 36.36000061035156, 36.36000061035156, 50.209999084472656], 'date': ['2021-12-01', '2022-03-16', '2022-06-10', '2022-07-13', '2022-08-22', '2022-08-22', '2023-02-24']},
    'VOO': {'num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'amount': [4, 2, 5, 4, 5, 13, 82, 20, 30, 67, 36, 3, 12, 4], 'price': [394.3135070800781, 394.1153869628906, 382.6412658691406, 385.9238586425781, 343.4385986328125, 365.70391845703125, 353.81121826171875, 403.1678771972656, 375.3546447753906, 455.4203186035156, 506.63482666015625, 494.16375732421875, 521.8684692382812, 537.4198608398438], 'date': ['2021-12-01', '2022-02-04', '2022-03-16', '2022-04-18', '2022-06-10', '2022-08-22', '2023-02-24', '2023-08-14', '2023-10-30', '2024-05-01', '2024-07-05', '2024-07-24', '2024-09-23', '2024-12-18']},
    'XLE': {'num': [1, 2], 'amount': [3, 4], 'price': [61.695091247558594, 61.695091247558594], 'date': ['2022-02-04', '2022-02-04']}
}

    ofer.tickers_sell_dict = {
    'AAPL': {'num': [1], 'amount': [2], 'price': [160.3211669921875], 'date': ['2022-02-24']},
    'ABNB': {'num': [1], 'amount': [2], 'price': [91.5], 'date': ['2022-12-07']},
    'ALB': {'num': [1], 'amount': [1], 'price': [237.40565490722656], 'date': ['2022-08-02']},
    'BITO': {'num': [1], 'amount': [12], 'price': [10.831171989440918], 'date': ['2022-02-24']},
    'CRSR': {'num': [1], 'amount': [17], 'price': [15.529999732971191], 'date': ['2022-12-07']},
    'QQQ': {'num': [1], 'amount': [64], 'price': [346.2629699707031], 'date': ['2023-10-30']},
    'TSM': {'num': [1], 'amount': [2], 'price': [83.39640045166016], 'date': ['2022-08-19']},
    'UAL': {'num': [1], 'amount': [3], 'price': [44.060001373291016], 'date': ['2022-02-24']},
    'VOO': {'num': [1], 'amount': [6], 'price': [376.20196533203125], 'date': ['2022-02-24']},
    'XLE': {'num': [1], 'amount': [7], 'price': [80.19336700439453], 'date': ['2022-06-10']}
}

    ofer.account_dict =  {
    'AAL': {'amount': 166, 'initial price': 14.924759324774685, 'current price': 18.290000915527344, 'stock value in portfolio': 3036.140151977539, 'price change': 558.6301040649414, 'percentage change': 22.54804595184628, 'percentage portfolio': 0.6018840586740825},
    'AAPL': {'amount': 141, 'initial price': 155.62203676480775, 'current price': 228.25999450683594, 'stock value in portfolio': 32184.659225463867, 'price change': 10241.952041625977, 'percentage change': 46.67588167593915, 'percentage portfolio': 6.380282975094937},
    'AMD': {'amount': 37, 'initial price': 82.65810538627007, 'current price': 118.44000244140625, 'stock value in portfolio': 4382.280090332031, 'price change': 1323.9301910400386, 'percentage change': 43.28903606963116, 'percentage portfolio': 0.8687426781987304},
    'BITO': {'amount': 411, 'initial price': 7.348538505479947, 'current price': 24.40999984741211, 'stock value in portfolio': 10032.509937286377, 'price change': 7012.260611534119, 'percentage change': 232.17489204430376, 'percentage portfolio': 1.988843563696812},
    'GOOGL': {'amount': 234, 'initial price': 99.90598407973592, 'current price': 192.91000366210938, 'stock value in portfolio': 45140.940856933594, 'price change': 21762.94058227539, 'percentage change': 93.0915404508163, 'percentage portfolio': 8.948734687903466},
    'INTC': {'amount': 114, 'initial price': 30.253219537567674, 'current price': 19.670000076293945, 'stock value in portfolio': 2242.3800086975098, 'price change': -1206.487018585205, 'percentage change': -34.982126276285264, 'percentage portfolio': 0.4445291433089503},
    'META': {'amount': 82, 'initial price': 252.78917508009005, 'current price': 611.2999877929688, 'stock value in portfolio': 50126.59899902344, 'price change': 29397.886642456055, 'percentage change': 141.8220588754615, 'percentage portfolio': 9.937090958534784},
    'MSFT': {'amount': 87, 'initial price': 265.8010236367412, 'current price': 424.5799865722656, 'stock value in portfolio': 36938.45883178711, 'price change': 13813.769775390625, 'percentage change': 59.73602387345234, 'percentage portfolio': 7.322675637473671},
    'NVDA': {'amount': 30, 'initial price': 22.49782346089681, 'current price': 133.57000732421875, 'stock value in portfolio': 4007.1002197265625, 'price change': 3332.165515899658, 'percentage change': 493.70190879297786, 'percentage portfolio': 0.7943670657601031},
    'QQQ': {'amount': 238, 'initial price': 409.2024525547607, 'current price': 513.0800170898438, 'stock value in portfolio': 122113.04406738281, 'price change': 24722.860359349754, 'percentage change': 25.385371931802343, 'percentage portfolio': 24.20767517350997},
    'SMH': {'amount': 51, 'initial price': 143.21882928586473, 'current price': 252.2899932861328, 'stock value in portfolio': 12866.789657592773, 'price change': 5562.629364013672, 'percentage change': 76.15700012640244, 'percentage portfolio': 2.550710834667338},
    'TSLA': {'amount': 50, 'initial price': 206.53653717041016, 'current price': 413.82000732421875, 'stock value in portfolio': 20691.000366210938, 'price change': 10364.17350769043, 'percentage change': 100.36164689968736, 'percentage portfolio': 4.101781424790464},
    'UAL': {'amount': 73, 'initial price': 39.744520631555005, 'current price': 106.11000061035156, 'stock value in portfolio': 7746.030044555664, 'price change': 4844.680038452148, 'percentage change': 166.98019984698456, 'percentage portfolio': 1.535572064679522},
    'VOO': {'amount': 281, 'initial price': 416.0546972743133, 'current price': 544.239990234375, 'stock value in portfolio': 152931.43725585938, 'price change': 36020.067321777344, 'percentage change': 30.809721365925725, 'percentage portfolio': 30.317109733707177}
}

    ofer.show_account_info()
    # print("2021:")
    # ofer.show_profit(ticker="all", start_date="2021-01-01", end_date="2022-01-01")
    # print("2022:")
    # ofer.show_profit(ticker="all", start_date="2022-01-01", end_date="2023-01-01")
    # print("2023:")
    # ofer.show_profit(ticker="all", start_date="2023-01-01", end_date="2024-01-01")
    # print("2024:")
    # ofer.show_profit(ticker="all", start_date="2024-01-01", end_date="2025-01-01")

if __name__ == '__main__':
    main()

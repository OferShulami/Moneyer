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

    #2021
    ofer.buy_stock("crsr", 17, date="2021-12-01")
    ofer.buy_stock("ual", 3, date="2021-12-01")
    ofer.buy_stock("abnb", 2, date="2021-12-01")
    ofer.buy_stock("meta", 1, date="2021-12-01")
    ofer.buy_stock("tsla", 1, date="2021-12-01") ###tsla split
    ofer.buy_stock("msft", 1, date="2021-12-01")
    ofer.buy_stock("aapl", 2, date="2021-12-01")
    ofer.buy_stock("voo", 4, date="2021-12-01")

    #2022
    #feb
    ofer.buy_stock("xle", 3, date="2022-02-04")
    ofer.buy_stock("bito", 12, date="2022-02-04")
    ofer.buy_stock("xle", 4, date="2022-02-04")
    ofer.buy_stock("meta", 1, date="2022-02-04")
    ofer.buy_stock("voo", 2, date="2022-02-04")
    ofer.sell_stock("ual", 3, date="2022-02-24")
    ofer.sell_stock("aapl", 2, date="2022-02-24")
    ofer.sell_stock("bito", 12, date="2022-02-24")
    ofer.sell_stock("voo", 6, date="2022-02-24")
    #march
    ofer.buy_stock("voo", 5, date="2022-03-16")
    ofer.buy_stock("bito", 13, date="2022-03-16")
    ofer.buy_stock("ual", 4, date="2022-03-16")
    ofer.buy_stock("aapl", 2, date="2022-03-16")
    #april
    ofer.buy_stock("aapl", 4, date="2022-04-18")
    ofer.buy_stock("bito", 24, date="2022-04-18")
    ofer.buy_stock("meta", 1, date="2022-04-18")
    ofer.buy_stock("aapl", 1, date="2022-04-18")
    ofer.buy_stock("voo", 4, date="2022-04-18")
    #june
    ofer.sell_stock("xle", 7, date="2022-06-10")
    ofer.buy_stock("qqq", 6, date="2022-06-10")
    ofer.buy_stock("smh", 7, date="2022-06-10")
    ofer.buy_stock("tsm", 2, date="2022-06-10")
    ofer.buy_stock("intc", 8, date="2022-06-10")
    ofer.buy_stock("amd", 2, date="2022-06-10")
    ofer.buy_stock("nvda", 2, date="2022-06-10")
    ofer.buy_stock("voo", 5, date="2022-06-10")
    ofer.buy_stock("aapl", 2, date="2022-06-10")
    ofer.buy_stock("msft", 1, date="2022-06-10")
    ofer.buy_stock("ual", 8, date="2022-06-10")
    ofer.buy_stock("meta", 1, date="2022-06-10")
    ofer.buy_stock("qqq", 1, date="2022-06-10")
    ofer.buy_stock("alb", 1, date="2022-06-22")
    #jule
    ofer.buy_stock("ual", 6, date="2022-07-13")
    #agust
    ofer.sell_stock("alb", 1, date="2022-08-02")
    ofer.sell_stock("tsm", 2, date="2022-08-19")
    ofer.buy_stock("ual", 21, date="2022-08-22")
    ofer.buy_stock("msft", 14, date="2022-08-22")
    ofer.buy_stock("aal", 57, date="2022-08-22")
    ofer.buy_stock("ual", 21, date="2022-08-22")
    ofer.buy_stock("intc", 57, date="2022-08-22")
    ofer.buy_stock("smh", 9, date="2022-08-22")
    ofer.buy_stock("tsla", 2, date="2022-08-22") ### check split
    ofer.buy_stock("nvda", 17, date="2022-08-22")
    ofer.buy_stock("qqq", 32, date="2022-08-22")
    ofer.buy_stock("voo", 13, date="2022-08-22")
    ofer.buy_stock("aapl", 31, date="2022-08-29")
    ofer.buy_stock("googl", 55, date="2022-08-29")
    #dec
    ofer.sell_stock("crsr", 17, date="2022-12-07")
    ofer.sell_stock("abnb", 2, date="2022-12-07")
    #2023
    #feb
    ofer.buy_stock("aal", 109, date="2023-02-24")
    ofer.buy_stock("ual", 13, date="2023-02-24")
    ofer.buy_stock("bito", 321, date="2023-02-24")
    ofer.buy_stock("tsla", 44, date="2023-02-24")
    ofer.buy_stock("amd", 31, date="2023-02-24")
    ofer.buy_stock("intc", 38, date="2023-02-24")
    ofer.buy_stock("nvda", 10, date="2023-02-24")
    ofer.buy_stock("smh", 13, date="2023-02-24")
    ofer.buy_stock("meta", 36, date="2023-02-24")
    ofer.buy_stock("googl", 156, date="2023-02-24")
    ofer.buy_stock("aapl", 88, date="2023-02-24")
    ofer.buy_stock("msft", 60, date="2023-02-24")
    ofer.buy_stock("qqq", 61, date="2023-02-24")
    ofer.buy_stock("voo", 82, date="2023-02-24")
    #aug
    ofer.buy_stock("smh", 14, date="2023-08-14")
    ofer.buy_stock("aapl", 6, date="2023-08-14")
    ofer.buy_stock("meta", 39, date="2023-08-14")
    ofer.buy_stock("intc", 11, date="2023-08-14")
    ofer.buy_stock("googl", 14, date="2023-08-14")
    ofer.buy_stock("tsla", 3, date="2023-08-14")
    ofer.buy_stock("amd", 4, date="2023-08-14")
    ofer.buy_stock("msft", 7, date="2023-08-14")
    ofer.buy_stock("bito", 43, date="2023-08-14")
    ofer.buy_stock("qqq", 45, date="2023-08-14")
    ofer.buy_stock("voo", 20, date="2023-08-14")
    #oc
    ofer.sell_stock("qqq", 64, date="2023-10-30")   ##################
    ofer.buy_stock("voo", 30, date="2023-10-30")
    #2024
    #may
    ofer.buy_stock("voo", 67, date="2024-05-01")
    ofer.buy_stock("qqq", 81, date="2024-05-01")
    #july
    ofer.buy_stock("voo", 36, date="2024-07-05")
    ofer.buy_stock("qqq", 41, date="2024-07-05")
    ofer.buy_stock("voo", 3, date="2024-07-24")
    ofer.buy_stock("qqq", 6, date="2024-07-24")
    ofer.buy_stock("smh", 8, date="2024-07-24")
    #sep
    ofer.buy_stock("voo", 12, date="2024-09-23")
    #nov
    ofer.buy_stock("qqq", 15, date="2024-11-12")
    #dec
    ofer.buy_stock("qqq", 5, date="2024-09-12")
    ofer.buy_stock("bito", 10, date="2024-09-12")
    ofer.buy_stock("nvda", 1, date="2024-09-12")
    ofer.buy_stock("qqq", 9, date="2024-12-18")
    ofer.buy_stock("voo", 4, date="2024-12-18")
    ofer.buy_stock("meta", 3, date="2024-12-18")
    ofer.buy_stock("googl", 9, date="2024-12-18")
    ofer.buy_stock("msft", 4, date="2024-12-18")
    ofer.buy_stock("aapl", 7, date="2024-12-18")
    
    

#check: TSLA, SMH. BITO. NVDA, UAL

#     ofer.tickers_buy_dict = {'CRSR': {'num': [1], 'amount': [17], 'price': [21.34000015258789], 'date': ['2021-12-01']}, 'UAL': {'num': [1, 2, 3, 4, 5, 6, 7], 'amount': [3, 4, 8, 6, 6, 21, 13], 'price': [39.060001373291016, 41.189998626708984, 41.15999984741211, 36.720001220703125, 36.720001220703125, 36.720001220703125, 50.209999084472656], 'date': ['2021-12-01', '2022-03-16', '2022-06-10', '2022-06-22', '2022-06-22', '2022-06-22', '2023-02-24']}, 'ABNB': {'num': [1], 'amount': [2], 'price': [163.0800018310547], 'date': ['2021-12-01']}, 'META': {'num': [1, 2, 3, 4, 5, 6, 7], 'amount': [1, 1, 1, 1, 36, 39, 3], 'price': [309.4180603027344, 236.18777465820312, 209.9679412841797, 174.90188598632812, 169.74160766601562, 305.02484130859375, 597.1900024414062], 'date': ['2021-12-01', '2022-02-04', '2022-04-18', '2022-06-10', '2023-02-24', '2023-08-14', '2024-12-18']}, 'TSLA': {'num': [1, 2, 3, 4], 'amount': [3, 2, 44, 3], 'price': [365.0, 236.086669921875, 196.8800048828125, 239.75999450683594], 'date': ['2021-12-01', '2022-06-22', '2023-02-24', '2023-08-14']}, 'MSFT': {'num': [1, 2, 3, 4, 5, 6], 'amount': [1, 1, 14, 60, 7, 4], 'price': [321.7357482910156, 247.6799774169922, 247.8170623779297, 245.81021118164062, 320.3052062988281, 437.3900146484375], 'date': ['2021-12-01', '2022-06-10', '2022-06-22', '2023-02-24', '2023-08-14', '2024-12-18']}, 'AAPL': {'num': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'amount': [2, 2, 4, 1, 2, 31, 88, 6, 7], 'price': [162.11447143554688, 157.2179412841797, 162.6165313720703, 162.6165313720703, 135.29029846191406, 137.3621063232422, 145.40493774414062, 178.35015869140625, 248.0500030517578], 'date': ['2021-12-01', '2022-03-16', '2022-04-18', '2022-04-18', '2022-06-10', '2022-06-29', '2023-02-24', '2023-08-14', '2024-12-18']}, 'VOO': {'num': [1, 2, 3, 4, 5, 6, 
# 7, 8, 9, 10, 11, 12, 13, 14], 'amount': [4, 2, 5, 4, 5, 13, 82, 20, 30, 67, 36, 3, 12, 4], 'price': [394.3134460449219, 394.11541748046875, 382.6412353515625, 385.9237976074219, 343.4385986328125, 331.19720458984375, 353.81121826171875, 403.1678771972656, 375.3546142578125, 455.4203186035156, 506.63482666015625, 494.1637268066406, 521.868408203125, 537.4198608398438], 'date': ['2021-12-01', '2022-02-04', '2022-03-16', '2022-04-18', '2022-06-10', '2022-06-22', '2023-02-24', '2023-08-14', '2023-10-30', '2024-05-01', '2024-07-05', '2024-07-24', '2024-09-23', '2024-12-18']}, 'XLE': {'num': [1, 2], 'amount': [3, 4], 'price': [61.69508743286133, 61.69508743286133], 'date': ['2022-02-04', '2022-02-04']}, 'BITO': {'num': 
# [1, 2, 3, 4, 5, 6], 'amount': [12, 13, 24, 321, 43, 10], 'price': [11.506431579589844, 11.551446914672852, 11.429902076721191, 6.558292388916016, 8.020267486572266, 14.567922592163086], 'date': ['2022-02-04', '2022-03-16', '2022-04-18', '2023-02-24', '2023-08-14', '2024-09-12']}, 'QQQ': {'num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'amount': [6, 1, 32, 61, 45, 81, 41, 6, 15, 5, 9], 'price': [283.42718505859375, 283.42718505859375, 275.93975830078125, 288.13507080078125, 366.7042541503906, 419.58392333984375, 494.66607666015625, 461.98480224609375, 512.084228515625, 471.795166015625, 515.6384887695312], 'date': ['2022-06-10', '2022-06-10', '2022-06-22', '2023-02-24', '2023-08-14', '2024-05-01', '2024-07-05', '2024-07-24', '2024-11-12', '2024-09-12', '2024-12-18']}, 'SMH': {'num': [1, 2, 3, 4, 5], 'amount': [7, 9, 13, 14, 8], 'price': [109.50363159179688, 102.00833892822266, 117.86896514892578, 149.09649658203125, 239.91664123535156], 'date': ['2022-06-10', '2022-06-22', '2023-02-24', '2023-08-14', '2024-07-24']}, 'TSM': {'num': [1], 'amount': [2], 'price': [84.36746978759766], 'date': ['2022-06-10']}, 'INTC': {'num': [1, 2, 3, 4], 'amount': [8, 57, 38, 11], 'price': [36.904380798339844, 35.20892333984375, 24.537330627441406, 35.09306716918945], 'date': ['2022-06-10', '2022-06-22', '2023-02-24', '2023-08-14']}, 'AMD': {'num': [1, 2, 3], 'amount': [2, 31, 4], 'price': [94.81999969482422, 78.08999633789062, 111.9800033569336], 'date': ['2022-06-10', '2023-02-24', '2023-08-14']}, 'NVDA': {'num': [1, 2, 3, 4], 'amount': [2, 17, 10, 1], 'price': [16.952287673950195, 16.339073181152344, 23.269075393676758, 119.13179016113281], 'date': ['2022-06-10', '2022-06-22', '2023-02-24', '2024-09-12']}, 'ALB': {'num': [1], 'amount': [1], 'price': [210.4907989501953], 'date': ['2022-06-22']}, 'AAL': {'num': [1, 2], 'amount': [67, 109], 'price': [13.100000381469727, 15.5600004196167], 'date': ['2022-06-22', '2023-02-24']}, 
# 'GOOGL': {'num': [1, 2, 3, 4], 'amount': [55, 156, 14, 9], 'price': [111.29803466796875, 88.80806732177734, 130.8556365966797, 188.39999389648438], 'date': ['2022-06-29', '2023-02-24', '2023-08-14', '2024-12-18']}}

#     ofer.tickers_sell_dict = {'UAL': {'num': [1], 'amount': [3], 'price': [44.060001373291016], 'date': ['2022-02-24']}, 'AAPL': {'num': [1], 'amount': [2], 'price': [160.3211669921875], 'date': ['2022-02-24']}, 'BITO': {'num': [1], 'amount': [12], 'price': [10.831170082092285], 'date': ['2022-02-24']}, 'VOO': {'num': [1], 'amount': [6], 'price': [376.2019348144531], 'date': ['2022-02-24']}, 'XLE': {'num': [1], 'amount': [7], 'price': [80.193359375], 'date': ['2022-06-10']}, 'ALB': {'num': [1], 'amount': [1], 'price': [237.40565490722656], 'date': ['2022-08-02']}, 'TSM': {'num': [1], 'amount': [2], 'price': [83.39641571044922], 'date': ['2022-08-19']}, 'CRSR': {'num': 
# [1], 'amount': [17], 'price': [15.529999732971191], 'date': ['2022-12-07']}, 'ABNB': {'num': [1], 'amount': [2], 'price': [91.5], 'date': ['2022-12-07']}, 'QQQ': {'num': [1], 'amount': [64], 'price': [346.26300048828125], 'date': ['2023-10-30']}}
    
#     ofer.account_dict =  {'META': {'amount': 82, 'initial price': 252.20324330049402, 'current price': 610.719970703125, 'stock value in portfolio': 51911.197509765625, 'price change': 30473.921829223633, 'percentage change': 142.15389251575445, 'percentage portfolio': 10.252900498842084}, 'TSLA': {'amount': 52, 'initial price': 210.56102958092322, 'current price': 394.94000244140625, 'stock value in portfolio': 20536.880126953125, 'price change': 9587.706588745117, 'percentage change': 87.56557337673073, 'percentage portfolio': 4.05620749663281}, 'MSFT': {'amount': 87, 'initial price': 261.8294686503794, 'current price': 424.55999755859375, 'stock value in portfolio': 36936.719787597656, 'price change': 14157.556015014648, 'percentage change': 62.151342149155965, 'percentage portfolio': 7.295314515998346}, 'VOO': {'amount': 281, 'initial price': 414.45829365686166, 'current price': 542.1400146484375, 'stock value in portfolio': 152341.34411621094, 'price change': 35878.56359863281, 'percentage change': 30.806892501778744, 'percentage portfolio': 30.08870374815641}, 'BITO': {'amount': 411, 'initial price': 7.3485378209691845, 'current price': 22.84000015258789, 'stock value in portfolio': 9387.240062713623, 'price change': 6366.991018295288, 'percentage change': 210.8101326962425, 'percentage portfolio': 1.8540592962364402}, 'UAL': {'amount': 58, 'initial price': 40.664310718404835, 'current price': 103.72000122070312, 'stock value in portfolio': 6015.760070800781, 'price change': 3657.230049133301, 'percentage change': 155.06395998926652, 'percentage portfolio': 1.188163486677888}, 'AAPL': {'amount': 141, 'initial price': 150.76886473310753, 'current price': 242.6999969482422, 'stock value in portfolio': 34220.69956970215, 'price change': 12962.289642333984, 'percentage change': 60.9748785850925, 'percentage portfolio': 6.758877554749524}, 'QQQ': {'amount': 238, 'initial price': 406.7146960939128, 'current price': 515.27001953125, 'stock value in portfolio': 122634.2646484375, 'price change': 25836.166978086258, 'percentage change': 26.690779674278396, 'percentage portfolio': 24.221304333281097}, 'SMH': {'amount': 51, 'initial price': 141.63884510713464, 'current price': 252.22999572753906, 'stock value in portfolio': 12863.729782104492, 'price change': 5640.148681640625, 'percentage change': 78.07967548503663, 'percentage portfolio': 2.5406954149939893}, 'INTC': {'amount': 114, 'initial price': 31.759526135628683, 'current price': 19.8799991607666, 'stock value in portfolio': 2266.3199043273926, 'price change': -1354.2660751342773, 'percentage change': -37.40461027072854, 'percentage portfolio': 0.44761734639704287}, 'AMD': {'amount': 37, 'initial price': 82.65810538627007, 'current price': 121.83999633789062, 'stock value in portfolio': 4508.079864501953, 'price change': 1449.7299652099605, 'percentage change': 47.40235790370399, 'percentage portfolio': 0.8903838961310202}, 'NVDA': {'amount': 30, 'initial price': 22.116378784179688, 'current price': 140.11000061035156, 'stock value in portfolio': 4203.300018310547, 'price change': 3539.8086547851562, 'percentage change': 533.5123935866716, 'percentage portfolio': 0.8301872991161849}, 'AAL': {'amount': 176, 'initial price': 14.623523132367568, 'current price': 17.600000381469727, 'stock value in portfolio': 3097.600067138672, 'price change': 523.85999584198, 'percentage change': 20.35403658995179, 'percentage portfolio': 0.6118022083309624}, 'GOOGL': {'amount': 234, 'initial price': 100.44029601007445, 'current price': 193.9499969482422, 'stock value in portfolio': 45384.29928588867, 'price change': 21881.27001953125, 'percentage change': 93.09978629372861, 'percentage portfolio': 8.9637829044562}}

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

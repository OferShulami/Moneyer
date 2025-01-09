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

    # #2021
    # ofer.buy_stock("crsr", 17, date="2021-12-01")
    # ofer.buy_stock("ual", 3, date="2021-12-01")
    # ofer.buy_stock("abnb", 2, date="2021-12-01")
    # ofer.buy_stock("meta", 1, date="2021-12-01")
    # ofer.buy_stock("tsla", 3, date="2021-12-01")
    # ofer.buy_stock("msft", 1, date="2021-12-01")
    # ofer.buy_stock("aapl", 2, date="2021-12-01")
    # ofer.buy_stock("voo", 4, date="2021-12-01")

    # #2022
    # ofer.buy_stock("xle", 3, date="2022-02-04")
    # ofer.buy_stock("bito", 12, date="2022-02-04")
    # ofer.buy_stock("xle", 4, date="2022-02-04")
    # ofer.buy_stock("meta", 4, date="2022-02-04")
    # ofer.buy_stock("voo", 2, date="2022-02-04")
    # #feb
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
    # ofer.buy_stock("ual", 6, date="2022-06-22")
    # #agust
    # ofer.sell_stock("alb", 1, date="2022-08-02")
    # ofer.buy_stock("ual", 6, date="2022-06-22")
    # ofer.sell_stock("tsm", 2, date="2022-08-19")
    # ofer.buy_stock("msft", 14, date="2022-06-22")
    # ofer.buy_stock("aal", 67, date="2022-06-22")
    # ofer.buy_stock("ual", 21, date="2022-06-22")
    # ofer.buy_stock("intc", 57, date="2022-06-22")
    # ofer.buy_stock("smh", 9, date="2022-06-22")
    # ofer.buy_stock("tsla", 2, date="2022-06-22")
    # ofer.buy_stock("nvda", 17, date="2022-06-22")
    # ofer.buy_stock("qqq", 32, date="2022-06-22")
    # ofer.buy_stock("voo", 13, date="2022-06-22")
    # ofer.buy_stock("aapl", 31, date="2022-06-29")
    # ofer.buy_stock("googl", 55, date="2022-06-29")
    # #dec
    # ofer.sell_stock("crsr", 17, date="2022-12-07")
    # ofer.sell_stock("abnb", 2, date="2022-12-07")

    ofer.tickers_buy_dict = {
        'CRSR': {
            'num': [1],
            'amount': [17], 
            'price': [21.34000015258789], 
            'date': ['2021-12-01']
            }, 
        'UAL': {
            'num': [1, 2, 3, 4, 5, 6], 
            'amount': [3, 4, 8, 6, 6, 21], 
            'price': [39.060001373291016, 41.189998626708984, 41.15999984741211, 36.720001220703125, 36.720001220703125, 36.720001220703125], 
            'date': ['2021-12-01', '2022-03-16', '2022-06-10', '2022-06-22', '2022-06-22', '2022-06-22']
            },
        'ABNB': {
            'num': [1], 
            'amount': [2], 
            'price': [163.0800018310547], 
            'date': ['2021-12-01']
            }, 
        'META': {
            'num': [1, 2, 3, 4], 
            'amount': [1, 4, 1, 1], 
            'price': [309.4180603027344, 236.1877899169922, 209.9679412841797, 174.90188598632812], 
            'date': ['2021-12-01', '2022-02-04', '2022-04-18', '2022-06-10']
            }, 
        'TSLA': {
            'num': [1, 2], 
            'amount': [3, 2], 
            'price': [365.0, 236.086669921875], 
            'date': ['2021-12-01', '2022-06-22']
            }, 
        'MSFT': {
            'num': [1, 2, 3], 
            'amount': [1, 1, 14], 
            'price': [321.7357177734375, 247.67999267578125, 247.81703186035156], 
            'date': ['2021-12-01', '2022-06-10', '2022-06-22']
            }, 
        'AAPL': {
            'num': [1, 2, 3, 4, 5, 6], 
            'amount': [2, 2, 4, 1, 2, 31], 
            'price': [162.11444091796875, 157.21800231933594, 162.61654663085938, 162.61654663085938, 135.290283203125, 137.3621063232422], 
            'date': ['2021-12-01', '2022-03-16', '2022-04-18', '2022-04-18', '2022-06-10', '2022-06-29']
            }, 
        'VOO': {
            'num': [1, 2, 3, 4, 5, 6], 
            'amount': [4, 2, 5, 4, 5, 13], 
            'price': [394.3134460449219, 394.11541748046875, 382.6412353515625, 385.9238586425781, 343.43853759765625, 331.197265625], 
            'date': ['2021-12-01', '2022-02-04', '2022-03-16', '2022-04-18', '2022-06-10', '2022-06-22']
            }, 
        'XLE': {
            'num': [1, 2], 
            'amount': [3, 4], 
            'price': [61.69509506225586, 61.69509506225586], 
            'date': ['2022-02-04', '2022-02-04']
            }, 
        'BITO': {
            'num': [1, 2, 3], 
            'amount': [12, 13, 24], 
            'price': [11.506433486938477, 11.551446914672852, 11.429903030395508], 
            'date': ['2022-02-04', '2022-03-16', '2022-04-18']
            }, 
        'QQQ': {
            'num': [1, 2, 3], 
            'amount': [6, 1, 32], 
            'price': [283.4271545410156, 283.4271545410156, 275.9397277832031], 
            'date': ['2022-06-10', '2022-06-10', '2022-06-22']
            }, 
        'SMH': {
            'num': [1, 2], 
            'amount': [7, 9], 
            'price': [109.50363159179688, 102.00833892822266], 
            'date': ['2022-06-10', '2022-06-22']
            }, 
        'TSM': {
            'num': [1], 
            'amount': [2], 
            'price': [84.36748504638672], 
            'date': ['2022-06-10']
            }, 
        'INTC': {
            'num': [1, 2], 
            'amount': [8, 57], 
            'price': [36.90437698364258, 35.20892333984375], 
            'date': ['2022-06-10', '2022-06-22']
            },
        'AMD': {
            'num': [1], 
            'amount': [2], 
            'price': [94.81999969482422], 
            'date': ['2022-06-10']
            },
        'NVDA': {
            'num': [1, 2], 
            'amount': [2, 17], 
            'price': [16.952289581298828, 16.339073181152344], 
            'date': ['2022-06-10', '2022-06-22']
            }, 
        'ALB': {
            'num': [1], 
            'amount': [1], 
            'price': [210.4907989501953], 
            'date': ['2022-06-22']
            }, 
        'AAL': {
            'num': [1], 
            'amount': [67], 
            'price': [13.100000381469727], 
            'date': ['2022-06-22']
            }, 
        'GOOGL': {
            'num': [1], 
            'amount': [55], 
            'price': [111.29803466796875], 
            'date': ['2022-06-29']
            }
        }

    ofer.tickers_sell_dict = {
        'UAL': {'num': [1], 'amount': [3], 'price': [44.060001373291016], 'date': ['2022-02-24']}, 'AAPL': {'num': [1], 'amount': [2], 'price': [160.32115173339844], 'date': ['2022-02-24']}, 'BITO': {'num': [1], 'amount': [12], 'price': [10.831171035766602], 'date': ['2022-02-24']}, 'VOO': {'num': [1], 'amount': [6], 'price': [376.20196533203125], 'date': ['2022-02-24']}, 'XLE': {'num': [1], 'amount': [7], 'price': [80.193359375], 'date': ['2022-06-10']}, 'ALB': {'num': [1], 'amount': 
[1], 'price': [237.40565490722656], 'date': ['2022-08-02']}, 'TSM': {'num': [1], 'amount': [2], 'price': [83.39640808105469], 'date': ['2022-08-19']}, 'CRSR': 
{'num': [1], 'amount': [17], 'price': [15.529999732971191], 'date': ['2022-12-07']}, 'ABNB': {'num': [1], 'amount': [2], 'price': [91.5], 'date': ['2022-12-07']}}
    
    ofer.account_dict =  {
        'META': {'amount': 7, 'initial price': 234.14843532017298, 'current price': 610.719970703125, 'stock value in portfolio': 4275.039794921875, 'price change': 2636.000747680664, 'percentage change': 160.82598838127217, 'percentage portfolio': 5.145901828539824}, 'TSLA': {'amount': 5, 'initial price': 313.43466796875, 'current price': 394.94000244140625, 'stock value in portfolio': 1974.7000122070312, 'price change': 407.52667236328125, 'percentage change': 26.003930899176254, 'percentage portfolio': 2.376963231009987}, 'MSFT': {'amount': 16, 'initial price': 252.4283847808838, 'current price': 424.55999755859375, 'stock value in portfolio': 6792.9599609375, 'price change': 2754.1058044433594, 'percentage change': 68.19027619541515, 'percentage portfolio': 8.176743787439971}, 'VOO': {'amount': 27, 'initial price': 351.0984723126447, 'current price': 542.1400146484375, 'stock value in portfolio': 14637.780395507812, 'price change': 5158.121643066406, 'percentage change': 54.41252451980907, 'percentage portfolio': 17.6196209898403}, 'BITO': {'amount': 37, 'initial price': 11.472607638384845, 'current price': 22.84000015258789, 'stock value in portfolio': 845.080005645752, 'price change': 420.5935230255127, 'percentage change': 99.08290139872148, 'percentage portfolio': 1.0172300036786885}, 'UAL': {'amount': 45, 'initial price': 37.90666741265191, 'current price': 103.72000122070312, 'stock value in portfolio': 4667.400054931641, 'price change': 2961.6000213623047, 'percentage change': 173.61941394532886, 'percentage portfolio': 5.618189216795003}, 'AAPL': {'amount': 40, 'initial price': 141.40811500549316, 'current price': 242.6999969482422, 'stock value in portfolio': 9707.999877929688, 'price change': 4051.675277709961, 'percentage change': 71.63088337526756, 'percentage portfolio': 11.685602174427407}, 'QQQ': {'amount': 39, 'initial price': 277.2836248935797, 'current price': 515.27001953125, 'stock value in portfolio': 20095.53076171875, 'price change': 9281.46939086914, 'percentage change': 85.82778544135394, 'percentage portfolio': 24.1891616108562}, 'SMH': {'amount': 16, 'initial price': 105.28752946853638, 'current price': 252.22999572753906, 'stock value in portfolio': 4035.679931640625, 'price change': 2351.079460144043, 'percentage change': 139.56302992455934, 'percentage portfolio': 4.857782321535202}, 'INTC': {'amount': 65, 'initial price': 35.41759455754207, 'current price': 19.8799991607666, 'stock value in portfolio': 1292.199945449829, 'price change': -1009.9437007904053, 'percentage change': -43.86970823648661, 'percentage portfolio': 1.555432085106673}, 'AMD': {'amount': 2, 'initial price': 94.81999969482422, 'current price': 121.83999633789062, 'stock value in portfolio': 243.67999267578125, 'price change': 54.03999328613281, 'percentage change': 28.496094421039427, 'percentage portfolio': 0.2933196835684167}, 'NVDA': {'amount': 19, 'initial price': 16.403622275904606, 'current price': 140.11000061035156, 'stock value in portfolio': 2662.0900115966797, 'price change': 2350.421188354492, 'percentage change': 754.1406175644516, 'percentage portfolio': 3.2043804304898393}, 'AAL': {'amount': 67, 'initial price': 13.100000381469727, 'current price': 17.600000381469727, 'stock value in portfolio': 1179.2000255584717, 'price change': 301.5, 'percentage change': 34.351144037868586, 'percentage portfolio': 1.4194131186669896}, 'GOOGL': {'amount': 55, 'initial price': 111.29803466796875, 'current price': 193.9499969482422, 'stock value in portfolio': 10667.24983215332, 'price change': 4545.857925415039, 'percentage change': 74.26183447609469, 'percentage portfolio': 12.840259518045501}}


    print(f"account: {ofer.account_dict}\n")
    print(f"sell: {ofer.tickers_sell_dict}\n")
    print(f"buy: {ofer.tickers_buy_dict}\n")

    #ofer.show_account_info()
    print("2021:")
    ofer.show_profit(ticker="all", start_date="2021-01-01", end_date="2022-01-01")
    # # print("2022:")
    # # ofer.show_profit(ticker="all", start_date="2022-01-01", end_date="2023-01-01")


if __name__ == '__main__':
    main()

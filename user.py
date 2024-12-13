import calculate_func


class Account:
    def __init__(self, name: str, password: str) -> None:
        self.__type__ = "Account"  # Add __type__ attribute to identify this class as "Account"
        self.name = name
        self.password = password
        self.tickers_buy_dict = {}
        # tickers_buy_dict = {
        #    ticker1(str): {
        #        "num": [1, 2...(int)],
        #        "amount": [10, 13...(int)],
        #        "price": [3000, 31231...(float)],
        #        "date": ["2023-12-01", "2024-03-04"...(str)]
        #    }
        # }
        self.tickers_sell_dict = {}
        # tickers_sell_dict = {
        #    ticker1(str): {
        #        "num": [1, 2...(int)],
        #        "amount": [10, 13...(int)],
        #        "price": [3000, 31231...(float)],
        #        "date": ["2023-12-01", "2024-03-04"...(str)]
        #    }
        # }
        self.account_dict = {}
        # accounts_dict = {
        #    ticker1(str): {
        #       "amount": 10 (int),
        #       "initial price": 31.231 (float),
        #       "current price": 34.233 (float),
        #       "stock value in Portfolio": current price * amount (float)
        #       "Price Change": stock value in Portfolio - initial price * amount
        #       "Percentage Change": ( current price - initial price ) / initial price * 100
        #       "percentage portfolio": (value of ticker / sum of all) * 100
        #    }
        # }

    def __repr__(self):
        return f"Account(name={self.name}, __type__={self.__type__})"

    def buy_stock(self, ticker: str, amount: int, price_per_stock: float = None, buy_date: str = None) -> None:
        """
        Add to the tickers_buy_dict this info: [amount(int), price(float), date(str, YYYY-MM-DD)].
        :param ticker: str
        :param amount: int
        :param price_per_stock: float / None
        :param buy_date: str (optional)
        :return: None
        """
        ticker = ticker.upper()

        #check if there is enough data
        if price_per_stock is None and buy_date is None:
            raise ValueError(f"You are missing the date or price.")

        #check if ticker is valid
        if not calculate_func.is_valid_ticker(ticker):
            raise ValueError(f"This ticker {ticker} is invalid.")

        if not calculate_func.check_date(buy_date):
            raise ValueError(f"This buy date {buy_date} is invalid.")

        if ticker not in self.tickers_buy_dict:
            self.tickers_buy_dict[ticker] = {
                "num": [],
                "amount": [],
                "price": [],
                "date": []
            }

        #update the ticker buy dict
        calculate_func.super_update(self.tickers_buy_dict, ticker, amount, price_per_stock, buy_date)
        #update the account dict
        self.account_dict = calculate_func.update_account_dict(True, ticker, self.account_dict, self.tickers_sell_dict,
                                                               self.tickers_buy_dict)

    def sell_stock(self, ticker: str, amount: int, price_per_stock: float = None, sell_date: str = None) -> None:
        """
        Add to the tickers_sale_dict this info: [amount(int), price(float), date(str, YYYY-MM-DD)].
        :param ticker: str
        :param amount: int
        :param price_per_stock: float / None
        :param sell_date: str (optional)
        :return: None
        """
        # Ensure the ticker exists in the dictionary
        if ticker not in self.tickers_buy_dict:
            raise ValueError(f"you don't have this ticker in your account: {ticker}")

        if ticker not in self.tickers_sell_dict:
            self.tickers_sell_dict[ticker] = {
                "num": [],
                "amount": [],
                "price": [],
                "date": []
            }

        if price_per_stock is None and sell_date is None:
            raise ValueError(f"You are missing the date or price.")

        calculate_func.super_update(self.tickers_sell_dict, ticker, amount, price_per_stock, sell_date)

    def show_buy_info(self):
        calculate_func.show_order_info(self.tickers_buy_dict)

    def show_sell_info(self):
        calculate_func.show_order_info(self.tickers_sell_dict)

    def show_account_info(self):
        calculate_func.create_account_sum(self.account_dict)
        calculate_func.make_account_table(self.account_dict)


def main():
    
    calculate_func.setup_pd()
    ofer = Account("guy", "1234")
    ofer.buy_stock("nvda", 1, buy_date="2024-12-10")
    ofer.buy_stock("aapl", 1, buy_date="2024-12-10")
    ofer.buy_stock("voo", 1, buy_date="2024-12-10")

    #ofer.show_buy_info()


    ofer.show_account_info()


if __name__ == '__main__':
    main()

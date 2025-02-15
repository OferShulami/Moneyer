import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import pandas_market_calendars as mcal

def setup_pd() -> None:

    pd.set_option('display.width', 1000)  # Set a wide display width
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns
    return None

def find_end_time(start_date: str) -> str:
    """
    Find the next date based on a given start date after validation.

    parameters:
    start_date (str): The starting date in YYYY-MM-DD format.

    Returns:
    str: The next valid date in the same format.

    Raises:
    ValueError: If there is any issue with the start date or date calculation.
    """
    try:
        end_time = calculate_next_date(start_date)  # calculate the next date
        return end_time
    except ValueError as e:
        raise ValueError(f"Error in finding end time: {e}")

def calculate_next_date(date_string: str, date_format: str = "%Y-%m-%d") -> str:
    """
    calculates the next date given a date string and returns it in the same format.

    parameters:
    date_string (str): The starting date as a string.
    date_format (str): The format of the input date string (default: 'YYYY-MM-DD').

    Returns:
    str: The next date as a string in the same format.

    Raises:
    ValueError: If the input date is invalid or doesn't match the expected format.

    Example:
    calculate_next_date("2023-12-31")
    '2024-01-01'
    """
    try:
        # parse the input date
        given_date = datetime.strptime(date_string, date_format)
        # Add one day
        next_date = given_date + timedelta(days=1)
        # Return the next date in the same format
        return next_date.strftime(date_format)
    except ValueError as e:
        raise ValueError(f"Invalid date or format: {e}")

def sub_date(start_date: str, end_date: str) -> tuple:
    

    start_date = sub_date_halper(start_date)
    end_date = sub_date_halper(end_date)

    return (start_date, end_date)

def sub_date_halper(date: str) -> str:
    
    while True:

        try:
            date = check_date(date)
            break            
        except Exception:
            date = datetime.strptime(date, "%Y-%m-%d")
            date = date - timedelta(days=1) 
            date = date.strftime("%Y-%m-%d")

    return date

def check_date(start_date: str) -> str:
    """

    :param start_date:
    :return:
    """

    fix_start_date = fix_date_format(start_date)
    if fix_start_date == "Error":
        raise ValueError(f"Invalid date format: {start_date}")
    
    if check_start_date(fix_start_date):
        return fix_start_date
    else:
        raise ValueError("check_date")

def check_start_date(start_date: str) -> bool:
    """
    Validates the start date and ensures it is after the NASDAQ founding date (1971-02-08).

    parameters:
    start_date (str): The start date in YYYY-MM-DD format.

    Returns:
    bool: The valid start date.

    Raises:
    ValueError: If the date is invalid or before NASDAQ's founding.
    """
    start_year_NASDAQ = 1971
    start_month_NASDAQ = 2
    start_day_NASDAQ = 8

    # Ensure the date is after NASDAQ's founding date (1971-02-08)
    nasdaq_start_date = datetime(start_year_NASDAQ, start_month_NASDAQ, start_day_NASDAQ)
    parsed_date = datetime.strptime(start_date, "%Y-%m-%d")

    if parsed_date < nasdaq_start_date:
        raise ValueError(f"The NASDAQ stock market did not exist before {nasdaq_start_date.strftime('%Y-%m-%d')}.")


    if start_date in get_nasdaq_open_days(start_date, start_date):
        return True

    else:
        raise ValueError(f"The NASDAQ stock market was close on {start_date}.")

def fix_date_format(date_string: str) -> str:
    """
    Tries to fix a date string that may be in various formats and return it in the standard 'YYYY-MM-DD' format.

    The function attempts to parse the input date string using a list of common date formats.
    If the string matches any of these formats, it is converted into the 'YYYY-MM-DD' format.
    If no valid format is found, the function returns 'Invalid date format'.
    :param date_string: A string representing a date, possibly in a non-standard format.
    :return: The date in 'YYYY-MM-DD' format if successfully parsed, otherwise 'Invalid date format'.
    """

    # Define a list of possible date formats
    possible_formats = [
        "%Y-%m-%d",  # YYYY-MM-DD
        "%d/%m/%Y",  # DD/MM/YYYY
        "%m/%d/%Y",  # MM/DD/YYYY
        "%Y/%m/%d",  # YYYY/MM/DD
        "%d-%m-%Y",  # DD-MM-YYYY
        "%m-%d-%Y",  # MM-DD-YYYY
        "%Y.%m.%d",  # YYYY.MM.DD
    ]

    for date_format in possible_formats:
        try:
            # Try parsing the date with each possible format
            parsed_date = datetime.strptime(date_string, date_format)
            # Return the date in the correct YYYY-MM-DD format
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            # If the date doesn't match the current format, continue to the next format
            continue

    # If none of the formats match, return an error message or None
    return "Error"

def get_nasdaq_open_days(start_date, end_date):
    """
    Get the days the NASDAQ is open between two dates.

    :param start_date: str, start date in 'YYYY-MM-DD' format.
    :param end_date: str, end date in 'YYYY-MM-DD' format.
    :return: List of open dates (as strings).
    """
    # Load NASDAQ calendar
    nasdaq = mcal.get_calendar('NASDAQ')

    # Get schedule for the specified range
    schedule = nasdaq.schedule(start_date=start_date, end_date=end_date)

    # Convert the index (open days) to a list of strings
    open_days = schedule.index.strftime('%Y-%m-%d').tolist()

    return open_days

def find_prices(the_ticker: str, start_date: str) -> list:
    """
    Fetch the stock's open, high, low, close prices, and volume for a specific date.
    Returns a list of prices or None if no data is available.
    """
    end_date = find_end_time(start_date)

    try:
        # Fetch stock data
        stock = yf.Ticker(the_ticker)
        data = stock.history(start=start_date, end=end_date, interval='1d')
        
        if data.empty:
            raise Exception(f"No trading data for {the_ticker} on {start_date}.")
            
        # Extract specific columns
        open_price = data['Open'].iloc[0]
        high_price = data['High'].iloc[0]
        low_price = data['Low'].iloc[0]
        close_price = data['Close'].iloc[0]
        volume = data['Volume'].iloc[0]

        return [open_price, high_price, low_price, close_price, volume]

    except Exception as e:
        print(f"Error: {e}")
        
def is_valid_ticker(ticker: str) -> bool:
    """
    checks if a ticker symbol is valid by attempting to fetch its data using yfinance.

    parameters:
        ticker (str): The ticker symbol to validate.

    Returns:
        bool: True if the ticker is valid, False otherwise.
    """
    try:
        # create a Ticker object
        stock = yf.Ticker(ticker)

        # Use get_info to fetch ticker information
        info = stock.get_info()

        # check if 'shortName' exists and is non-empty
        return 'shortName' in info and bool(info['shortName'])
    except Exception as e:
        # Log or handle exceptions if needed
        print(f"Error validating ticker '{ticker}': {e}")
        return False

def now_date() -> str:
    """
    Gets the current date in 'YYYY-MM-DD' format.

    Returns:
        str: Today's date as a string in 'YYYY-MM-DD' format.
    """
    # Get today's date and format it as a string
    today_date = datetime.now().strftime("%Y-%m-%d")

    return today_date

def profit(ticker: str, start_date: str, end_date: str, tickers_buy_dict: dict, tickers_sell_dict: dict, account_dict: dict, profit_dict) -> dict:
    ticker = ticker.upper()
    start_account_dict = {}
    profit: float = 0
    initial_invest: float = 0

    # Convert to datetime variables
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    start_account_dict = create_start_account_dict(ticker, start_date, tickers_buy_dict, tickers_sell_dict, initial_invest, start_account_dict)
    
    profit_dict = update_initial_profit_dict(start_account_dict, profit_dict, ticker)

    initial_invest = start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]

    timeline = create_timeline(ticker, start_date, end_date, tickers_buy_dict, tickers_sell_dict)

    sorted_timeline = sorted(timeline, key=lambda x: x[4])

    for action in sorted_timeline:

        profit += go_over_action(start_account_dict, action, profit)
        if action[0] == "buy":
            initial_invest += action[2] * action[3]
            if profit_dict[action[1]]["initial price"] == 0:
                profit_dict[action[1]]["initial price"] = action[3]
            if profit_dict[action[1]]["initial amount"] == 0:
                profit_dict[action[1]]["initial amount"] = action[2]     
            if profit_dict[action[1]]["initial stock value in Portfolio"] == 0:
                 profit_dict[action[1]]["initial stock value in Portfolio"] = profit_dict[action[1]]["initial amount"] * profit_dict[action[1]]["initial price"] 


    profit_dict = update_final_profit_dict(start_account_dict, profit_dict, profit, initial_invest, ticker)

    return profit_dict

def update_final_profit_dict(start_account_dict: dict, profit_dict: dict, profit: float, initial_invest: float, ticker: str) -> dict:

    keys_to_remove = []
    for key in profit_dict:
        if profit_dict[key]["initial price"] == 0:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del profit_dict[key]

    if ticker in keys_to_remove:
        pass
    else:
        profit_dict[ticker]["final amount"] = start_account_dict[ticker]["amount"]
        profit_dict[ticker]["final price"] = start_account_dict[ticker]["current price"]
        profit_dict[ticker]["final stock value in Portfolio"] = start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]
        profit_dict[ticker]["profit"] = profit
        profit_dict[ticker]["percentage change"] = profit / (initial_invest) * 100

    return profit_dict

def update_initial_profit_dict(start_account_dict: dict, profit_dict: dict, ticker: str) -> dict:


    profit_dict = reset_profit_dict(profit_dict, ticker)

    profit_dict[ticker]["initial amount"] = start_account_dict[ticker]["amount"]
    profit_dict[ticker]["initial price"] = start_account_dict[ticker]["initial price"]
    profit_dict[ticker]["initial stock value in Portfolio"] = start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]

    return profit_dict
        
def reset_profit_dict(profit_dict: dict, ticker: str) -> dict:
    
    profit_dict[ticker] = {

        "initial amount": 0,
        "final amount": 0,
        "initial price": 0,
        "final price": 0,
        "initial stock value in Portfolio": 0,
        "final stock value in Portfolio": 0,
        "profit": 0, 
        "percentage change": 0,
        "percentage in portfolio": 0,
    }

    return profit_dict

def go_over_action(start_account_dict: dict, action: tuple, profit: float) -> float:



    if action[0] == "buy":

        old_amount = start_account_dict[action[1]]["amount"]
        old_price = start_account_dict[action[1]]["current price"]
        new_current_price = action[3]

            
        start_account_dict[action[1]]["amount"] += action[2]
        start_account_dict[action[1]]["initial price"] = new_current_price
        start_account_dict[action[1]]["current price"] = new_current_price
        start_account_dict[action[1]]["stock value in Portfolio"] = new_current_price * start_account_dict[action[1]]["amount"]
        start_account_dict[action[1]]["Price Change"] = 0
        start_account_dict[action[1]]["percentage change"] = 0
        start_account_dict[action[1]]["percentage portfolio"] = 0

        if old_amount == 0:
            profit = 0
                    
        else:

            profit = (new_current_price - old_price) * old_amount



    elif action[0] == "sell":

        old_amount = start_account_dict[action[1]]["amount"]
        old_price = start_account_dict[action[1]]["current price"]
        new_current_price = action[3]


        start_account_dict[action[1]]["amount"] -= action[2]
        start_account_dict[action[1]]["initial price"] = new_current_price
        start_account_dict[action[1]]["current price"] = new_current_price
        start_account_dict[action[1]]["stock value in Portfolio"] = new_current_price * start_account_dict[action[1]]["amount"]
        start_account_dict[action[1]]["Price Change"] = 0
        start_account_dict[action[1]]["percentage change"] = 0
        start_account_dict[action[1]]["percentage portfolio"] = 0


        profit = (new_current_price - old_price) * action[2] * 0.75 + (new_current_price - old_price) * start_account_dict[action[1]]["amount"]




    elif action[0] == "end":
        
        old_price = start_account_dict[action[1]]["current price"]
        new_current_price = bring_price(find_prices(action[1], action[4].strftime("%Y-%m-%d")), 'close')

        
        start_account_dict[action[1]]["initial price"] = new_current_price
        start_account_dict[action[1]]["current price"] = new_current_price
        start_account_dict[action[1]]["stock value in Portfolio"] = new_current_price * start_account_dict[action[1]]["amount"]
        start_account_dict[action[1]]["Price Change"] = 0
        start_account_dict[action[1]]["percentage change"] = 0
        start_account_dict[action[1]]["percentage portfolio"] = 0

        profit = (new_current_price - old_price) * start_account_dict[action[1]]["amount"]



    else: 
        raise Exception("Error in timeline!")
    
    
    return profit    

def create_timeline(ticker: str, start_date: datetime, end_date: datetime, tickers_buy_dict: dict, tickers_sell_dict: dict) -> list:

    timeline = []
    #[order, ticker, amount, price, date)]

    if ticker not in tickers_buy_dict: 
        pass
    
    else:
        for i in range(len(tickers_buy_dict[ticker]["amount"])):

            date = datetime.strptime(tickers_buy_dict[ticker]["date"][i], "%Y-%m-%d")
            if date >= start_date and date <= end_date:
                timeline.append(("buy", ticker, tickers_buy_dict[ticker]["amount"][i], tickers_buy_dict[ticker]["price"][i], date))

    if ticker not in tickers_sell_dict: 
        pass
    
    else:
        for i in range(len(tickers_sell_dict[ticker]["amount"])):

            date = datetime.strptime(tickers_sell_dict[ticker]["date"][i], "%Y-%m-%d")
            if date >= start_date and date <= end_date:
                timeline.append(("sell", ticker, tickers_sell_dict[ticker]["amount"][i], tickers_sell_dict[ticker]["price"][i], date))

    timeline.append(("end", ticker, 0, 0, end_date))
                    
    return timeline

def create_relevent_buy_dict(ticker: str, start_date: datetime, tickers_buy_dict: dict,) -> list:

    relevent_buy_info = []

    if ticker not in tickers_buy_dict: 
        return relevent_buy_info
    else:

        for i in range(len(tickers_buy_dict[ticker]["date"])):
            the_date = datetime.strptime(tickers_buy_dict[ticker]["date"][i], "%Y-%m-%d")
            
            # Filter dates that are >= start_date
            if the_date <= start_date:
                relevent_buy_info.append(tickers_buy_dict[ticker]["amount"][i])
                

        return relevent_buy_info

def create_relevent_sell_dict(ticker: str, start_date: datetime, ticker_sell_dict: dict) -> list:

    relevent_sell_info = []

    if ticker not in ticker_sell_dict:
        return relevent_sell_info

    else:
        for i in range(len(ticker_sell_dict[ticker]["date"])):
            the_date = datetime.strptime(ticker_sell_dict[ticker]["date"][i], "%Y-%m-%d")
        
            # Filter dates that are >= start_date
            if the_date <= start_date:
                relevent_sell_info.append(ticker_sell_dict[ticker]["amount"][i])
            

    return relevent_sell_info

def create_start_account_dict(ticker: str, start_date: datetime, tickers_buy_dict: dict, tickers_sell_dict: dict, initial_invest: float, start_account_dict: dict) -> dict:

    start_account_dict[ticker] = {

        "amount": 0,
        "initial price": 0,
        "current price": 0,
        "stock value in Portfolio": 0,
        "Price Change": 0,
        "percentage change": 0, 
        "percentage portfolio": 0
        }
    a: int = 0

    relevent_buy_dict = create_relevent_buy_dict(ticker,start_date, tickers_buy_dict)
    relevent_sell_dict = create_relevent_sell_dict(ticker,start_date, tickers_sell_dict)

    for amount in relevent_buy_dict:
        start_account_dict[ticker]["amount"] += amount
    
    for amount in relevent_sell_dict:
        start_account_dict[ticker]["amount"] -= amount


    while True:

        try:
            if a > 9:
                start_account_dict[ticker]["current price"] = 0
                break
            else:
                start_account_dict[ticker]["current price"] = bring_price(find_prices(ticker, start_date.strftime("%Y-%m-%d")), 'close')
                break
        except Exception:
            a += 1
            start_date = start_date - timedelta(days=1) 

    start_account_dict[ticker]["stock value in Portfolio"] =  start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]
    if start_account_dict[ticker]["amount"] != 0:
        start_account_dict[ticker]["initial price"] = start_account_dict[ticker]["current price"]
    else:
       start_account_dict[ticker]["initial price"] = 0
        

    return start_account_dict

def update_dict_ticker_num(ticker: str, tickers_dict: dict) -> int:
    """
    Updates the ticker number to a given ticker symbol.
    :param ticker:
    :param tickers_dict:
    :return: num to add to ticker symbol
    """
    num = tickers_dict[ticker]["num"]
    if not num:
        num = 1
        return num
    else:
        next_num = num[-1] + 1
        return next_num

def update_dict_ticker(ticker: str, num: int, amount: int, stock_price: float, buy_sell_date: str,
                       tickers_dict: dict) -> None:
    """
    Update the dictionary with stock data.
    :param ticker: str
    :param num: int
    :param amount: int
    :param stock_price: float
    :param buy_date: str
    :param tickers_dict: dict (to store the data)
    :return: None
    """
    tickers_dict[ticker]["num"].append(num)
    tickers_dict[ticker]["amount"].append(amount)
    tickers_dict[ticker]["price"].append(stock_price)
    tickers_dict[ticker]["date"].append(buy_sell_date)

    return None

def bring_price(lst: list, order: str) -> float:
    """
    return the price according the given order.
    :param lst: the return of find_prices.
    :param order: high, open, close, low, volume
    :return: float price
    """
    if order == "open":
        return lst[0]
    if order == "high":
        return lst[1]
    if order == "low":
        return lst[2]
    if order == "close":
        return lst[3]
    if order == "volume":
        return lst[4]

    raise ValueError(f"Invalid order: {order}")

def round_numeric_values(data: dict) -> dict:
    for outer_key, inner_dict in data.items():
        for key, value in inner_dict.items():
            if isinstance(value, (float, np.float64)):
                inner_dict[key] = round(value, 3)

    return data

def make_account_table(data: dict) -> None:

    """
    creates a formatted table from a nested dictionary containing stock portfolio data.
    parameters:
    :param data: A nested dictionary where the outer keys represent stock tickers,
                 and the inner dictionaries contain details like amount, initial price,
                 current price, and percentage change.
    :return: None
    """
    data = round_numeric_values(data)
    profit_key_list = ['initial amount', 'final amount', 'initial price', 'final price', 'initial stock value in Portfolio', 'final stock value in Portfolio', 'profit', 'percentage change', 'percentage in portfolio']
    account_key_list = ['amount', 'initial price', 'stock value in portfolio', 'price change', 'percentage change', 'percentage portfolio', 'current price']
    data_key_list = []

    for key in data["total"]:
        data_key_list.append(key)        

    if data_key_list == account_key_list:
        refresh_current_price_in_account_dict(data)
        # Round numerical values to 3 decimal places
        for outer_key, inner_dict in data.items():
            for key, value in inner_dict.items():
                if isinstance(value, (float, np.float64)):
                    inner_dict[key] = round(value, 3)

        # create a DataFrame
        table = pd.DataFrame.from_dict(data, orient='index')

        # Use tabulate to print the table with lines
        table_with_lines_center = tabulate(table, headers='keys', tablefmt='grid', numalign='center', stralign='center')

        print(f"account info:\n{table_with_lines_center}")

    elif data_key_list == profit_key_list:
        # Create a DataFrame
        table = pd.DataFrame.from_dict(data, orient="index")
        table.index.name = "Stock Ticker"
        table.reset_index(inplace=True)

        # Rename columns for readability
        table.columns = [
            "Ticker", "Init Amt", "Final Amt", "Init Price", 
            "Final Price", "Init Value", "Final Value", "Profit", 
            "% Change", "% Portfolio"
        ]

        # Use tabulate for compact formatting
        table_with_lines = tabulate(
            table,
            headers="keys",
            tablefmt="fancy_grid",
            numalign="right",
            stralign="center",
        )

        print(f"profit:\n{table_with_lines}")

    else:

        raise("error in make account dict")  

def refresh_current_price_in_account_dict(account_dict: dict) -> None:
    """
    Refreshes the current price of each stock in the account dictionary.

    This function updates the "current price" field for each stock in the portfolio by
    fetching the latest price using the `get_current_price` function.

    :param account_dict: dict
                         A dictionary containing details about the portfolio. Each key is a stock ticker,
                         and the value is a dictionary with at least the following fields:
                         - "current price": The most recent market price of the stock.
    :return: None
             This function modifies the `account_dict` in place and does not return any value.
    """

    for ticker in account_dict:
        if ticker == 'total':
            continue
        else:
            account_dict[ticker]["current price"] = get_current_price(ticker)
        
    
    return None

def make_order_table(data: dict) -> str:
    """
    Creates a formatted table from a dictionary containing order data.

    :param data: A dictionary where keys represent column headers, and values are lists of data.
    :return: A string representation of the formatted table.
    """
    # Create a DataFrame
    table = pd.DataFrame.from_dict(data, orient="index").T  # Transpose to make rows into columns

    # Use tabulate to create the formatted table without index
    table_with_lines_center = tabulate(
        table,
        headers="keys",  # Use column names as headers
        tablefmt="grid",
        numalign="center",
        stralign="center",
        showindex=False,  # Disable the index column
    )

    # Return the table as a string
    return table_with_lines_center

def super_update(tickers_dict: dict, ticker: str, amount: int, price_per_stock: float = None, date: str = None) -> None:
    """
    Updates a stock data dictionary with a new purchase or price information.

    This function adds a new entry or updates an existing one in the tickers_dict
    for a given stock ticker. It calculates the stock price if not provided and
    handles the date of purchase.
    :param tickers_dict: A dictionary where each key is a ticker symbol, and the
                         value is another dictionary containing stock details.
    :param ticker: The stock ticker symbol (e.g., "AApL").
    :param amount: The number of shares purchased.
    :param price_per_stock: The price per stock. If None, it fetches
                            the closing price for the given date.
    :param date: The purchase date in "YYYY-MM-DD" format. If None, the
                 current date is used.
    :return: None
    """
    num = update_dict_ticker_num(ticker, tickers_dict)

    if price_per_stock is None:
        stock_price = bring_price(find_prices(ticker, date), "close")
        if date is None:
            date = now_date()
            update_dict_ticker(ticker, num, amount, stock_price, date, tickers_dict)
        else:
            update_dict_ticker(ticker, num, amount, stock_price, date, tickers_dict)
    else:
        stock_price = price_per_stock
        if date is None:
            date = now_date()
        update_dict_ticker(ticker, num, amount, stock_price, date, tickers_dict)

def show_order_info(tickers_dict: dict, order: str) -> None:
    """
    Displays detailed order information for each stock ticker in the provided dictionary.

    This function iterates through the `tickers_dict`, extracts information for each ticker
    (amount, price, and date of transactions), and prints it in a tabulated format.

    :param tickers_dict: A dictionary where each key is a stock ticker symbol, and the value
                         is another dictionary containing lists of amounts, prices, and dates
                         of transactions for that ticker.
    :return: None
    """
    if order == "buy":
        print("your buying info:\n")
    elif order == "sell":
        print("your selling info:\n")
    
    else:
        raise ValueError("go back to user.show_info")
    
    for ticker in tickers_dict:
        print(f"{ticker}:")
        data = {
            "num": tickers_dict[ticker]["num"],
            "amount": tickers_dict[ticker]["amount"],
            "price": tickers_dict[ticker]["price"],
            "date": tickers_dict[ticker]["date"],
        }

        # Call make_order_table and print the result
        print(make_order_table(data), "\n")

def get_current_price(ticker_symbol: str) -> float | None:
    """
    Fetches the current price of a stock using the yfinance library.

    parameters:
    ticker_symbol (str): The stock ticker symbol (e.g., 'AApL', 'GOOGL').

    Returns:
    float: The current stock price.

    Raises:
    ValueError: If the ticker symbol is invalid or data is unavailable.
    """
    try:
        # create a Ticker object
        if ticker_symbol == "total":
            return None
        stock = yf.Ticker(ticker_symbol)

        # Use fast_info for quick access to the current price
        current_price = stock.fast_info["last_price"]
        return current_price
    except KeyError:
        raise ValueError(f"could not retrieve the price for ticker '{ticker_symbol}'.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

def update_account_dict(order: bool, ticker: str, account_dict: dict, sell_dict: dict = None,
                        buy_dict: dict = None) -> dict:
    """
    Updates the account dictionary to reflect changes from a buy or sell order.

    The function modifies the `account_dict` based on whether a buy or sell operation is performed.
    It calculates and updates stock values, price changes, and percentage changes for each stock
    in the portfolio. For buy operations, it also calculates weighted average prices for new purchases.

    :param order: Indicates the type of order.
                  `True` for buy, `False` for sell.
    :param ticker: The stock ticker symbol for which the operation is performed.

    :param account_dict: The main dictionary holding portfolio details, where keys are stock tickers and values
                         are dictionaries with stock-related information.
    :param sell_dict: A dictionary containing sell order details (amounts and prices for the `ticker`).
                      Defaults to None.
    :param buy_dict: A dictionary containing buy order details (amounts and prices for the `ticker`).
                     Defaults to None.


    -------
    dict
        The updated `account_dict` reflecting the changes made by the order.

    Raises:
    ------
    ValueError
        If both `sell_dict` and `buy_dict` are None, since one is required to update the account.

    Notes:
    ------
    - The function calculates the following metrics:
        * Stock value in portfolio.
        * price change (absolute).
        * percentage change (relative to the initial price).
    - If the order is a buy and the stock already exists in the account, the initial price is
      recalculated as a weighted average.
    - calls `update_percentage_portfolio` to adjust portfolio-wide percentage metrics.

    Returns: None
        """

    # check if both sell_dict and buy_dict are None
    if sell_dict is None and buy_dict is None:
        raise ValueError("You are missing dict")




    current_price = get_current_price(ticker)



    # check if it's a buy order
    if order:

        new_amount = buy_dict[ticker]["amount"][-1]
        new_price = buy_dict[ticker]["price"][-1]
        
        # If account_dict doesn't have the ticker
        if ticker not in account_dict:
            # Update account dict by creating new ticker
            account_dict[ticker] = {}
            account_dict[ticker]["amount"] = new_amount
            account_dict[ticker]["initial price"] = new_price
            account_dict[ticker]["current price"] = current_price
            account_dict[ticker]["stock value in portfolio"] = new_amount * current_price
            account_dict[ticker]["price change"] = (current_price * new_amount) - (
                    new_price * new_amount)
            account_dict[ticker]["percentage change"] = ((current_price - new_price) /
                                                         new_price) * 100

        # If account_dict has this ticker
        else:


            old_amount = account_dict[ticker]["amount"]
            old_initial_price = account_dict[ticker]["initial price"]

            total_amount = old_amount + new_amount

            # Update values in account_dict
            account_dict[ticker]["amount"] = total_amount
            account_dict[ticker]["initial price"] = ((old_initial_price * old_amount) + (new_price * new_amount)) / total_amount
            account_dict[ticker]["current price"] = current_price
            account_dict[ticker]["stock value in portfolio"] = total_amount * current_price
            account_dict[ticker]["price change"] = (current_price * total_amount) - (
                    account_dict[ticker]["initial price"] * total_amount)
            account_dict[ticker]["percentage change"] = ((current_price - account_dict[ticker]["initial price"]) /
                                                         account_dict[ticker]["initial price"]) * 100
    # check if it's a sell order
    else:
            
        new_amount = sell_dict[ticker]["amount"][-1]
        new_price = sell_dict[ticker]["price"][-1]
        old_amount = account_dict[ticker]["amount"]
        total_amount = old_amount - new_amount

        if total_amount == 0:
            del account_dict[ticker]
        
        elif total_amount < 0:
            raise ValueError("cant sold more stocks")
        
        elif total_amount > 0:

            account_dict[ticker]["amount"] = total_amount
            account_dict[ticker]["current price"] = current_price
            account_dict[ticker]["stock value in portfolio"] = total_amount * current_price
            account_dict[ticker]["price change"] = (current_price * total_amount) - (
            account_dict[ticker]["initial price"] * total_amount)
            account_dict[ticker]["percentage change"] = ((current_price - account_dict[ticker]["initial price"]) /
                                                         account_dict[ticker]["initial price"]) * 100

        else: 
            raise ValueError("error")        


    update_percentage_portfolio(account_dict)

    return account_dict

def update_percentage_portfolio(account_dict: dict) -> None:
    """
    Updates the percentage of each stock's value relative to the total portfolio value.

    The function calculates the total value of the portfolio by summing the stock values
    and then updates the "percentage portfolio" for each stock in the `account_dict`.

    :param account_dict: The dictionary containing details about the portfolio.
                         Each key is a stock ticker, and its value is a dictionary with details such as
                         "stock value in portfolio" and other metrics.

    Notes:
    ------
    - Assumes the presence of a "stock value in portfolio" field in `account_dict` for all tickers.
    - The "percentage portfolio" value is stored as a percentage (0-100).
    - calls `calculate_sum_portfolio` to compute the total portfolio value.
    :return: None
             Updates the `account_dict` in place.
    """

    sum_val = calculate_sum_portfolio(account_dict)
    for ticker in account_dict:
        account_dict[ticker]["percentage portfolio"] = account_dict[ticker]["stock value in portfolio"] / sum_val * 100

def calculate_sum_portfolio(account_dict: dict) -> float:
    """
    calculates the total value of the portfolio by summing the stock values of all tickers.

    This function iterates through each ticker in the `account_dict` and adds up the
    "stock value in portfolio" for each one to compute the total portfolio value.

    :param account_dict: The dictionary containing details about the portfolio.
                         Each key is a stock ticker, and its value is a dictionary with at least the
                         "stock value in portfolio" field.
    :return: The total value of the portfolio, computed as the sum of "stock value in portfolio"
             for each ticker.
    """

    portfolio_sum_value = 0
    for ticker in account_dict:
        portfolio_sum_value += account_dict[ticker]["stock value in portfolio"]

    return portfolio_sum_value

def create_account_sum(account_dict: dict) -> None:
    """
    Calculates and adds a summary of the portfolio to the account dictionary.

    This function computes the total amount of stocks, the average initial price,
    the total value of the portfolio, the total price change, and the percentage change
    for all the stocks in the portfolio. It then adds these summary values to a new entry
    in the `account_dict` under the key "SUM".
    :param account_dict: dict
        A dictionary containing details about the portfolio. Each key is a stock ticker,
        and the value is a dictionary with information about that stock, such as:
        - "amount": The amount of shares owned
        - "initial price": The price at which the stock was initially purchased
        - "stock value in portfolio": The current value of the stock in the portfolio
        - "price change": The change in price for that stock
    :return: None
        This function modifies the `account_dict` in place by adding the summary under the key "SUM".
    """

    total_amount_of_stock = calculate_total_amount_of_stock(account_dict)
    average_initial_price = calculate_average_initial_price(account_dict)
    total_value_in_portfolio = calculate_total_value_in_portfolio(account_dict)
    total_price_change = calculate_total_price_change(account_dict)
    percentage_change = calculate_percentage_change(average_initial_price, total_amount_of_stock,
                                                    total_value_in_portfolio)
    average_current_price = calculate_average_current_price(total_value_in_portfolio, total_amount_of_stock)

    account_dict["total"] = {}

    account_dict["total"]["amount"] = total_amount_of_stock
    account_dict["total"]["initial price"] = average_initial_price
    account_dict["total"]['stock value in portfolio'] = total_value_in_portfolio
    account_dict["total"]['price change'] = total_price_change
    account_dict['total']['percentage change'] = percentage_change
    account_dict['total']['percentage portfolio'] = 100
    account_dict['total']['current price'] = average_current_price

    return None

def calculate_average_current_price(total_value_in_portfolio: float, total_amount_of_stock: int) -> float:
    """

    :param total_value_in_portfolio:
    :param total_amount_of_stock:
    :return:
    """

    average_current_price = total_value_in_portfolio / total_amount_of_stock
    return average_current_price

def calculate_percentage_change(average_initial_price: float, total_amount_of_stock: int,
                                total_value_in_portfolio: float) -> float:
    """
    Calculates and adds a summary of the portfolio to the account dictionary.

    This function computes the total amount of stocks, the average initial price,
    the total value of the portfolio, the total price change, and the percentage change
    for all the stocks in the portfolio. It then adds these summary values to a new entry
    in the `account_dict` under the key "SUM".


    :param average_initial_price:
    :param total_amount_of_stock:
    :param total_value_in_portfolio:
    :return: None
        This function modifies the `account_dict` in place by adding the summary under the key "SUM".
    """

    percentage_change = (total_value_in_portfolio - (average_initial_price * total_amount_of_stock)) * 100 / (
            average_initial_price * total_amount_of_stock)
    return percentage_change

def calculate_total_price_change(account_dict: dict) -> float:
    """
    calculates the total price change for all stocks in the portfolio.

    This function sums up the "Price change" for each stock in the `account_dict`
    to calculate the total price change of the portfolio.

    :param account_dict: dict
        A dictionary containing details about the portfolio. Each key is a stock ticker,
        and the value is a dictionary that includes the following field:
        - "Price change": The change in price for the stock, typically calculated as:
          (current price * amount) - (initial price * amount)
    :return:    float
        The total price change for the portfolio, which is the sum of the "Price change"
        for all tickers in the `account_dict`.
    """

    total_price_change = 0
    for ticker in account_dict:
        total_price_change += account_dict[ticker]["price change"]

    return total_price_change

def calculate_total_value_in_portfolio(account_dict: dict) -> float:
    """
    calculates the total value of all stocks in the portfolio.

    This function sums up the "stock value in portfolio" for each stock in the
    `account_dict` to calculate the total value of the portfolio.

    :param account_dict: dict
        A dictionary containing details about the portfolio. Each key is a stock ticker,
        and the value is a dictionary with at least the following fields:
        - "stock value in portfolio": The total value of the stock in the portfolio
          (calculated as amount * current price).
    :return: float
        The total value of the portfolio, which is the sum of the "stock value in portfolio"
        for all the tickers in the `account_dict`.
    """

    total_value_in_portfolio = 0
    for ticker in account_dict:
        total_value_in_portfolio += account_dict[ticker]["stock value in portfolio"]
    return total_value_in_portfolio

def calculate_average_initial_price(account_dict: dict) -> float:
    """
    calculates the average initial price of the stocks in the portfolio.

    The average initial price is computed by summing the initial prices for each stock
    multiplied by the number of shares held for that stock, and then dividing by the total
    amount of stocks in the portfolio.

    :param account_dict: A dictionary containing details about the portfolio. Each key is a stock ticker,
                         and the value is a dictionary with at least the following fields:
                         - "amount": The quantity of stocks held for that ticker.
                         - "price": The initial price of the stock at the time it was purchased.
    :return: The average initial price of all the stocks in the portfolio.
    """

    total_initial_price = 0
    for ticker in account_dict:
        total_initial_price += account_dict[ticker]["amount"] * account_dict[ticker]["initial price"]

    average_initial_price = total_initial_price / calculate_total_amount_of_stock(account_dict)
    return average_initial_price

def calculate_total_amount_of_stock(account_dict: dict) -> int:
    """
    calculates the total amount of stock in the portfolio by summing the amount of each stock.

    This function iterates through each ticker in the `account_dict` and adds up the
    "amount" for each ticker to compute the total amount of stocks in the portfolio.

    :param account_dict: The dictionary containing details about the portfolio.
                         Each key is a stock ticker, and its value is a dictionary with at least the
                         "amount" field, which represents the quantity of stock held for that ticker.

    :return: The total amount of stock in the portfolio, computed as the sum of "amount"
             for each ticker.
    """

    total_amount_of_stock = 0
    for ticker in account_dict:
        total_amount_of_stock += account_dict[ticker]["amount"]

    return total_amount_of_stock

def calculate_total_amount_of_stock_profit(profit_dict: dict) -> tuple:


    total_amount_of_initial_stock: int = 0
    total_amount_of_final_stock: int = 0
    for ticker in profit_dict:
        total_amount_of_initial_stock += profit_dict[ticker]["initial amount"]
        total_amount_of_final_stock += profit_dict[ticker]["final amount"]

    return (total_amount_of_initial_stock, total_amount_of_final_stock)

def calculate_total_value_in_portfolio_profit(profit_dict: dict) -> tuple:

    total_initial_value_in_portfolio: float = 0
    total_final_value_in_portfolio: float = 0
    for ticker in profit_dict:

        total_initial_value_in_portfolio += profit_dict[ticker]["initial stock value in Portfolio"]
        total_final_value_in_portfolio += profit_dict[ticker]["final stock value in Portfolio"]
    return (total_initial_value_in_portfolio, total_final_value_in_portfolio) 

def calculate_average_price_of_stock_profit(profit_dict: dict, total_amount_of_initial_stock: int, total_amount_of_final_stock: int) -> tuple:
    """
    Calculates the average initial and final stock prices based on the profit dictionary.

    Args:
        profit_dict (dict): Dictionary containing stock profit details for each ticker.
        total_amount_of_initial_stock (int): Total initial stock amount across all tickers.
        total_amount_of_final_stock (int): Total final stock amount across all tickers.

    Returns:
        tuple: Average initial price and average final price as floats.
    """
    total_initial_price: float = 0
    total_final_price: float = 0

    for ticker in profit_dict:
        total_initial_price += profit_dict[ticker]["initial amount"] * profit_dict[ticker]["initial price"]
        total_final_price += profit_dict[ticker]["final amount"] * profit_dict[ticker]["final price"]

    # Calculate average initial price
    if total_amount_of_initial_stock > 0:
        average_initial_price = total_initial_price / total_amount_of_initial_stock
    else:
        average_initial_price = profit_dict[ticker]["initial price"]  # Default value if no initial stock

    # Calculate average final price
    if total_amount_of_final_stock > 0:
        average_final_price = total_final_price / total_amount_of_final_stock
    else:
        average_final_price = 0  # Default value if no final stock

    return average_initial_price, average_final_price

def calculate_profit_sum(profit_dict: dict) -> float:

    total_profit: float = 0
    for ticker in profit_dict:
        total_profit += profit_dict[ticker]["profit"]

    return total_profit

def calculate_percentage_change_profit(profit_dict: dict) -> float:

    percentage_change: float = 0
    for key in profit_dict:
        percentage_change += profit_dict[key]["percentage change"] * profit_dict[key]["percentage in portfolio"] / 100
    
    return percentage_change

def update_percentage_in_portfolio(profit_dict: dict, total_final_value_in_portfolio: float) -> dict:
    for key in profit_dict:
        profit_dict[key]["percentage in portfolio"] = profit_dict[key]["final stock value in Portfolio"] / total_final_value_in_portfolio * 100 

    return profit_dict

def create_all_profit_dict(profit_dict: dict) -> dict:

    (total_amount_of_initial_stock, total_amount_of_final_stock) = calculate_total_amount_of_stock_profit(profit_dict)
    (average_initial_price, average_final_price) = calculate_average_price_of_stock_profit(profit_dict, total_amount_of_initial_stock, total_amount_of_final_stock)
    (total_initial_value_in_portfolio, total_final_value_in_portfolio) = calculate_total_value_in_portfolio_profit(profit_dict)
    total_profit = calculate_profit_sum(profit_dict)
    profit_dict = update_percentage_in_portfolio(profit_dict, total_final_value_in_portfolio)
    percentage_change = calculate_percentage_change_profit(profit_dict)
    
    

    profit_dict["total"] = {

        "initial amount": 0,
        "final amount": 0,
        "initial price": 0,
        "final price": 0,
        "initial stock value in Portfolio": 0,
        "final stock value in Portfolio": 0,
        "profit": 0, 
        "percentage change": 0,
        "percentage in portfolio": 0,
    }

    profit_dict["total"]["initial amount"] = total_amount_of_initial_stock
    profit_dict["total"]["final amount"] = total_amount_of_final_stock
    profit_dict["total"]["initial price"] = average_initial_price
    profit_dict["total"]["final price"] = average_final_price
    profit_dict["total"]['initial stock value in Portfolio'] = total_initial_value_in_portfolio
    profit_dict["total"]['final stock value in Portfolio'] = total_final_value_in_portfolio
    profit_dict["total"]['profit'] = total_profit
    profit_dict['total']['percentage change'] = percentage_change
    profit_dict['total']['percentage in portfolio'] = 100


    return profit_dict

def main():
    print("hell yes")

if __name__ == "__main__":
    main()

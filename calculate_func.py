import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import pandas_market_calendars as mcal


def setup_pd() -> None:
    """
    Configures Pandas display options to ensure tables are fully visible in the terminal.

    Adjusts the output width and removes limits on displayed rows and columns
    to prevent data truncation during portfolio reporting.
    """
    pd.set_option('display.width', 1000)  # Set a wide display width
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns

    return None
def find_end_time(start_date: str) -> str:
    """
    Calculates the next consecutive date based on a validated start date.

    Args:
        start_date (str): The starting date in 'YYYY-MM-DD' format.

    Returns:
        str: The following day's date in 'YYYY-MM-DD' format.

    Raises:
        ValueError: If the start_date is invalid or the date calculation fails.
    """
    try:
        # Calculate the next date using the helper function
        end_time = calculate_next_date(start_date)
        return end_time
    except ValueError as e:
        raise ValueError(f"Error in finding end time: {e}")
def calculate_next_date(date_string: str, date_format: str = "%Y-%m-%d") -> str:
    """
    Calculates the next consecutive date given a date string and returns it in the same format.

    Args:
        date_string (str): The starting date as a string.
        date_format (str): The format of the input date string (default: '%Y-%m-%d').

    Returns:
        str: The next date as a string in the same format.

    Raises:
        ValueError: If the input date is invalid or doesn't match the expected format.

    Example:
        >>> calculate_next_date("2023-12-31")
        '2024-01-01'
    """
    try:
        # Parse the input date string into a datetime object
        given_date = datetime.strptime(date_string, date_format)

        # Increment the date by exactly one day
        next_date = given_date + timedelta(days=1)

        # Return the resulting date formatted as the original input
        return next_date.strftime(date_format)
    except ValueError as e:
        raise ValueError(f"Invalid date or format: {e}")
def sub_date(start_date: str, end_date: str) -> tuple:
    """
    Standardizes and validates a pair of dates (start and end) using a helper function.

    This function ensures that both input dates are processed through the 'sub_date_helper'
    logic to handle business days, holidays, or formatting adjustments.

    Args:
        start_date (str): The initial start date string.
        end_date (str): The initial end date string.

    Returns:
        tuple: A tuple containing (processed_start_date, processed_end_date) as strings.
    """
    # Note: Corrected the typo from 'halper' to 'helper'
    start_date = sub_date_helper(start_date)
    end_date = sub_date_helper(end_date)

    return (start_date, end_date)
def sub_date_helper(date: str) -> str:
    """
    Adjusts a given date backwards until a valid trading day is found.

    This function attempts to validate a date. If validation fails (e.g., the market
    was closed), it subtracts one day and retries until 'check_date' succeeds.

    Args:
        date (str): The initial date string to validate and potentially adjust.

    Returns:
        str: The nearest valid trading date (in the past) in 'YYYY-MM-DD' format.
    """
    while True:
        try:
            # Attempt to validate the current date
            date = check_date(date)
            break
        except Exception:
            # If invalid (market closed or format issue), subtract one day and retry
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_obj = date_obj - timedelta(days=1)
            date = date_obj.strftime("%Y-%m-%d")

    return date
def check_date(start_date: str) -> str:
    """
    Validates the format and market status of a specific date.

    Args:
        start_date (str): The date string to be checked.

    Returns:
        str: The fixed date string in 'YYYY-MM-DD' format if valid.

    Raises:
        ValueError: If the date format is irreparable or the date is invalid
                    according to market rules.
    """
    # Attempt to fix common formatting issues
    fix_start_date = fix_date_format(start_date)

    if fix_start_date == "Error":
        raise ValueError(f"Invalid date format: {start_date}")

    # Verify if the date meets specific market start requirements
    if check_start_date(fix_start_date):
        return fix_start_date
    else:
        raise ValueError(f"Date validation failed for: {fix_start_date}")
def check_start_date(start_date: str) -> bool:
    """
    Validates that a date is post-NASDAQ founding (1971-02-08) and was a trading day.

    Args:
        start_date (str): The date string in 'YYYY-MM-DD' format.

    Returns:
        bool: True if the date is a valid NASDAQ trading day.

    Raises:
        ValueError: If the date is before NASDAQ founding or if the market was closed.
    """
    # NASDAQ founding date: February 8, 1971
    nasdaq_founding_date = datetime(1971, 2, 8)
    parsed_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Ensure the requested date is historically possible for NASDAQ data
    if parsed_date < nasdaq_founding_date:
        raise ValueError(
            f"The NASDAQ stock market did not exist before {nasdaq_founding_date.strftime('%Y-%m-%d')}."
        )

    # Check if the market was actually open on this specific day
    if start_date in get_nasdaq_open_days(start_date, start_date):
        return True
    else:
        raise ValueError(f"The NASDAQ stock market was closed on {start_date}.")
def fix_date_format(date_string: str) -> str:
    """
    Attempts to parse various date formats and standardize them to 'YYYY-MM-DD'.

    The function tries common international and US formats. If successful,
    it returns the standardized ISO string.

    Args:
        date_string (str): A string representing a date in an unknown format.

    Returns:
        str: Standardized 'YYYY-MM-DD' string, or "Error" if parsing fails.
    """
    # List of common formats to attempt parsing
    possible_formats = [
        "%Y-%m-%d",  # 2023-12-31
        "%d/%m/%Y",  # 31/12/2023
        "%m/%d/%Y",  # 12/31/2023
        "%Y/%m/%d",  # 2023/12/31
        "%d-%m-%Y",  # 31-12-2023
        "%m-%d-%Y",  # 12-31-2023
        "%Y.%m.%d",  # 2023.12.31
    ]

    for date_format in possible_formats:
        try:
            parsed_date = datetime.strptime(date_string, date_format)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Return "Error" as a sentinel value if no format matches
    return "Error"
def get_nasdaq_open_days(start_date: str, end_date: str) -> list:
    """
    Retrieves a list of actual trading days when NASDAQ was open between two dates.

    Args:
        start_date (str): Start date in 'YYYY-MM-DD'.
        end_date (str): End date in 'YYYY-MM-DD'.

    Returns:
        list: A list of strings representing open trading days.
    """
    # Load the official NASDAQ market calendar
    nasdaq_calendar = mcal.get_calendar('NASDAQ')

    # Fetch the market schedule for the specified range
    schedule = nasdaq_calendar.schedule(start_date=start_date, end_date=end_date)

    # Convert the resulting DatetimeIndex to a clean list of ISO date strings
    open_days = schedule.index.strftime('%Y-%m-%d').tolist()

    return open_days
def find_prices(ticker: str, start_date: str) -> list | None:
    """
    Fetches the stock's OHLCV (Open, High, Low, Close, Volume) data for a specific date.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): The target date in 'YYYY-MM-DD' format.

    Returns:
        list | None: A list containing [Open, High, Low, Close, Volume] as floats,
                     or None if data is unavailable or an error occurs.
    """
    # Determine the next day to define the 1-day interval for history()
    end_date = find_end_time(start_date)

    try:
        stock = yf.Ticker(ticker)
        # Fetch historical data for the specific day
        data = stock.history(start=start_date, end=end_date, interval='1d')

        if data.empty:
            raise ValueError(f"No trading data available for {ticker} on {start_date}.")

        # Extract specific columns using iloc and ensure float type
        open_price = float(data['Open'].iloc[0])
        high_price = float(data['High'].iloc[0])
        low_price = float(data['Low'].iloc[0])
        close_price = float(data['Close'].iloc[0])
        volume = float(data['Volume'].iloc[0])

        return [open_price, high_price, low_price, close_price, volume]

    except Exception as e:
        print(f"Error fetching prices for {ticker}: {e}")
        return None
def is_valid_ticker(ticker: str) -> bool:
    """
    Validates a ticker symbol by attempting to fetch its metadata from Yahoo Finance.

    Args:
        ticker (str): The ticker symbol to validate.

    Returns:
        bool: True if the ticker is recognized and has a valid profile, False otherwise.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetching ticker information to confirm its existence
        info = stock.get_info()

        # A valid ticker typically contains a 'shortName' identifier
        return 'shortName' in info and bool(info['shortName'])
    except Exception as e:
        print(f"Validation error for ticker '{ticker}': {e}")
        return False
def now_date() -> str:
    """
    Retrieves the current system date in a standardized format.

    Returns:
        str: Today's date formatted as 'YYYY-MM-DD'.
    """
    return datetime.now().strftime("%Y-%m-%d")
def profit(ticker: str, start_date_str: str, end_date_str: str,
           tickers_buy_dict: dict, tickers_sell_dict: dict,
           account_dict: dict, profit_dict: dict) -> dict:
    """
    Calculates the profit and performance metrics for a specific ticker over a given timeframe.

    This function reconstructs the portfolio state at the start date, processes a timeline
    of buy/sell actions during the period, and calculates the final profit and percentage change.

    Args:
        ticker (str): The stock ticker symbol.
        start_date_str (str): Calculation start date ('YYYY-MM-DD').
        end_date_str (str): Calculation end date ('YYYY-MM-DD').
        tickers_buy_dict (dict): Global dictionary of all buy transactions.
        tickers_sell_dict (dict): Global dictionary of all sell transactions.
        account_dict (dict): Current global account state.
        profit_dict (dict): The dictionary to be updated with calculation results.

    Returns:
        dict: The updated profit_dict containing metrics for the requested ticker.
    """
    ticker = ticker.upper()
    start_account_dict = {}
    current_profit: float = 0
    initial_invest: float = 0

    # Convert string dates to datetime objects for timeline processing
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Step 1: Establish the portfolio state as it was on the start_date
    start_account_dict = create_start_account_dict(
        ticker, start_date, tickers_buy_dict, tickers_sell_dict, initial_invest, start_account_dict
    )

    # Step 2: Initialize the profit dictionary with the starting values
    profit_dict = update_initial_profit_dict(start_account_dict, profit_dict, ticker)

    # Calculate initial investment value at the start of the period
    initial_invest = start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]

    # Step 3: Create and process a chronological timeline of all actions within the dates
    timeline = create_timeline(ticker, start_date, end_date, tickers_buy_dict, tickers_sell_dict)
    sorted_timeline = sorted(timeline, key=lambda x: x[4])

    for action in sorted_timeline:
        # Calculate profit contribution of each action (Buy/Sell/End)
        current_profit += go_over_action(start_account_dict, action, current_profit)

        # Track buy actions to update the 'initial investment' base for percentage calculations
        if action[0] == "buy":
            initial_invest += action[2] * action[3]

            # Fill in initial values if the stock was first acquired during this period
            if profit_dict[action[1]]["initial price"] == 0:
                profit_dict[action[1]]["initial price"] = action[3]
            if profit_dict[action[1]]["initial amount"] == 0:
                profit_dict[action[1]]["initial amount"] = action[2]
            if profit_dict[action[1]]["initial stock value in Portfolio"] == 0:
                profit_dict[action[1]]["initial stock value in Portfolio"] = (
                        profit_dict[action[1]]["initial amount"] * profit_dict[action[1]]["initial price"]
                )

    # Step 4: Finalize the dictionary with closing prices and final percentage changes
    profit_dict = update_final_profit_dict(start_account_dict, profit_dict, current_profit, initial_invest, ticker)

    return profit_dict
def update_final_profit_dict(start_account_dict: dict, profit_dict: dict,
                             profit_val: float, total_invested: float, ticker: str) -> dict:
    """
    Finalizes the profit dictionary entry for a ticker after processing the timeline.

    Args:
        start_account_dict (dict): The adjusted state of the account at the end of the period.
        profit_dict (dict): The dictionary being populated.
        profit_val (float): The total calculated profit/loss.
        total_invested (float): The total cost basis used for percentage calculation.
        ticker (str): The stock ticker symbol.

    Returns:
        dict: The profit_dict after cleanup and final calculations.
    """
    # Cleanup: Remove entries that didn't have a valid initial price (no holdings)
    keys_to_remove = [key for key in profit_dict if profit_dict[key]["initial price"] == 0]
    for key in keys_to_remove:
        del profit_dict[key]

    if ticker not in keys_to_remove:
        # Set final state metrics
        profit_dict[ticker]["final amount"] = start_account_dict[ticker]["amount"]
        profit_dict[ticker]["final price"] = start_account_dict[ticker]["current price"]
        profit_dict[ticker]["final stock value in Portfolio"] = (
                start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]
        )
        profit_dict[ticker]["profit"] = profit_val

        # Calculate ROI percentage for the period
        if total_invested != 0:
            profit_dict[ticker]["percentage change"] = (profit_val / total_invested) * 100
        else:
            profit_dict[ticker]["percentage change"] = 0

    return profit_dict
def update_initial_profit_dict(start_account_dict: dict, profit_dict: dict, ticker: str) -> dict:
    """
    Sets the baseline values in the profit dictionary at the start of the timeframe.

    Args:
        start_account_dict (dict): Account state at the start_date.
        profit_dict (dict): Dictionary to initialize.
        ticker (str): The stock ticker symbol.

    Returns:
        dict: The profit_dict with initial values set for the ticker.
    """
    # Reset/Initialize the specific ticker entry
    profit_dict = reset_profit_dict(profit_dict, ticker)

    # Capture state at the very beginning of the requested period
    profit_dict[ticker]["initial amount"] = start_account_dict[ticker]["amount"]
    profit_dict[ticker]["initial price"] = start_account_dict[ticker]["initial price"]
    profit_dict[ticker]["initial stock value in Portfolio"] = (
            start_account_dict[ticker]["amount"] * start_account_dict[ticker]["current price"]
    )

    return profit_dict
def reset_profit_dict(profit_dict: dict, ticker: str) -> dict:
    """
    Initializes or resets a ticker's entry in the profit dictionary with zeroed metrics.

    Args:
        profit_dict (dict): The dictionary storing profit metrics for various tickers.
        ticker (str): The stock ticker symbol to initialize.

    Returns:
        dict: The updated profit_dict with the new ticker structure.
    """
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
def go_over_action(start_account_dict: dict, action: tuple, accrued_profit: float) -> float:
    """
    Processes a single timeline action and calculates the resulting profit change.

    Handles three types of actions:
    1. 'buy': Updates holdings and calculates profit based on price movement since the last state.
    2. 'sell': Updates holdings and applies profit calculation (including a 25% cost/tax adjustment).
    3. 'end': Finalizes state at the end of the timeframe and calculates remaining unrealized profit.

    Args:
        start_account_dict (dict): The temporary account state during simulation.
        action (tuple): A tuple containing (order_type, ticker, amount, price, date).
        accrued_profit (float): The profit accumulated up to this point in the timeline.

    Returns:
        float: The incremental profit/loss generated by this specific action.

    Raises:
        ValueError: If an unknown action type is encountered in the timeline.
    """
    # Extract action details for clarity
    action_type = action[0]
    ticker = action[1]
    action_amount = action[2]
    action_price = action[3]
    action_date = action[4]

    incremental_profit = 0

    if action_type == "buy":
        old_amount = start_account_dict[ticker]["amount"]
        old_price = start_account_dict[ticker]["current price"]
        new_current_price = action_price

        # Update state
        start_account_dict[ticker]["amount"] += action_amount
        start_account_dict[ticker]["initial price"] = new_current_price
        start_account_dict[ticker]["current price"] = new_current_price
        start_account_dict[ticker]["stock value in Portfolio"] = new_current_price * start_account_dict[ticker][
            "amount"]

        # Reset relative metrics for the new cost basis
        start_account_dict[ticker].update({
            "Price Change": 0,
            "percentage change": 0,
            "percentage portfolio": 0
        })

        if old_amount > 0:
            incremental_profit = (new_current_price - old_price) * old_amount

    elif action_type == "sell":
        old_amount = start_account_dict[ticker]["amount"]
        old_price = start_account_dict[ticker]["current price"]
        new_current_price = action_price

        start_account_dict[ticker]["amount"] -= action_amount
        start_account_dict[ticker]["initial price"] = new_current_price
        start_account_dict[ticker]["current price"] = new_current_price
        start_account_dict[ticker]["stock value in Portfolio"] = new_current_price * start_account_dict[ticker][
            "amount"]

        start_account_dict[ticker].update({
            "Price Change": 0,
            "percentage change": 0,
            "percentage portfolio": 0
        })

        # Profit calculation includes a 0.75 multiplier (potential tax/fee adjustment)
        incremental_profit = (new_current_price - old_price) * action_amount * 0.75 + \
                             (new_current_price - old_price) * start_account_dict[ticker]["amount"]

    elif action_type == "end":
        old_price = start_account_dict[ticker]["current price"]
        # Fetch the actual closing price for the final date
        prices = find_prices(ticker, action_date.strftime("%Y-%m-%d"))
        new_current_price = bring_price(prices, 'close')

        start_account_dict[ticker]["initial price"] = new_current_price
        start_account_dict[ticker]["current price"] = new_current_price
        start_account_dict[ticker]["stock value in Portfolio"] = new_current_price * start_account_dict[ticker][
            "amount"]

        start_account_dict[ticker].update({
            "Price Change": 0,
            "percentage change": 0,
            "percentage portfolio": 0
        })

        incremental_profit = (new_current_price - old_price) * start_account_dict[ticker]["amount"]

    else:
        raise ValueError(f"Unknown action type '{action_type}' in timeline processing!")

    return incremental_profit
def create_timeline(ticker: str, start_date: datetime, end_date: datetime,
                    tickers_buy_dict: dict, tickers_sell_dict: dict) -> list:
    """
    Compiles a chronological list of buy and sell transactions for a specific ticker.

    Args:
        ticker (str): The stock ticker to track.
        start_date (datetime): The beginning of the period.
        end_date (datetime): The end of the period.
        tickers_buy_dict (dict): Dictionary containing purchase history.
        tickers_sell_dict (dict): Dictionary containing sales history.

    Returns:
        list: A list of tuples, each representing an action to be processed.
    """
    timeline = []

    # Process Buy transactions
    if ticker in tickers_buy_dict:
        for i in range(len(tickers_buy_dict[ticker]["amount"])):
            date_str = tickers_buy_dict[ticker]["date"][i]
            current_date = datetime.strptime(date_str, "%Y-%m-%d")

            if start_date <= current_date <= end_date:
                timeline.append((
                    "buy", ticker,
                    tickers_buy_dict[ticker]["amount"][i],
                    tickers_buy_dict[ticker]["price"][i],
                    current_date
                ))

    # Process Sell transactions
    if ticker in tickers_sell_dict:
        for i in range(len(tickers_sell_dict[ticker]["amount"])):
            date_str = tickers_sell_dict[ticker]["date"][i]
            current_date = datetime.strptime(date_str, "%Y-%m-%d")

            if start_date <= current_date <= end_date:
                timeline.append((
                    "sell", ticker,
                    tickers_sell_dict[ticker]["amount"][i],
                    tickers_sell_dict[ticker]["price"][i],
                    current_date
                ))

    # Append the termination point for the simulation
    timeline.append(("end", ticker, 0, 0, end_date))

    return timeline
def create_relevant_buy_dict(ticker: str, start_date: datetime, tickers_buy_dict: dict) -> list:
    """
    Filters purchase amounts for a ticker that occurred on or before a specific date.

    Args:
        ticker (str): The stock ticker symbol.
        start_date (datetime): The cutoff date for relevant transactions.
        tickers_buy_dict (dict): Global dictionary containing purchase history.

    Returns:
        list: A list of purchase amounts (integers) that are relevant to the start_date.
    """
    relevant_buy_amounts = []

    if ticker not in tickers_buy_dict:
        return relevant_buy_amounts

    # Iterate through dates and amounts simultaneously
    for date_str, amount in zip(tickers_buy_dict[ticker]["date"], tickers_buy_dict[ticker]["amount"]):
        transaction_date = datetime.strptime(date_str, "%Y-%m-%d")

        # Include transactions that happened on or before the reconstruction date
        if transaction_date <= start_date:
            relevant_buy_amounts.append(amount)

    return relevant_buy_amounts
def create_relevant_sell_dict(ticker: str, start_date: datetime, tickers_sell_dict: dict) -> list:
    """
    Filters sale amounts for a ticker that occurred on or before a specific date.

    Args:
        ticker (str): The stock ticker symbol.
        start_date (datetime): The cutoff date for relevant transactions.
        tickers_sell_dict (dict): Global dictionary containing sales history.

    Returns:
        list: A list of sale amounts (integers) that are relevant to the start_date.
    """
    relevant_sell_amounts = []

    if ticker not in tickers_sell_dict:
        return relevant_sell_amounts

    for date_str, amount in zip(tickers_sell_dict[ticker]["date"], tickers_sell_dict[ticker]["amount"]):
        transaction_date = datetime.strptime(date_str, "%Y-%m-%d")

        if transaction_date <= start_date:
            relevant_sell_amounts.append(amount)

    return relevant_sell_amounts
def create_start_account_dict(ticker: str, start_date: datetime,
                              tickers_buy_dict: dict, tickers_sell_dict: dict,
                              initial_invest: float, start_account_dict: dict) -> dict:
    """
    Reconstructs the account state (shares and price) for a ticker at a specific past date.

    Calculates the total shares held by summing all buys and subtracting all sells
    up to the start_date. It also searches back for the last valid market closing price.

    Args:
        ticker (str): The stock ticker symbol.
        start_date (datetime): The point in time to reconstruct.
        tickers_buy_dict (dict): Global purchase history.
        tickers_sell_dict (dict): Global sales history.
        initial_invest (float): Initial investment value (contextual).
        start_account_dict (dict): The dictionary to be populated with the reconstructed state.

    Returns:
        dict: The updated start_account_dict with the ticker's historical state.
    """
    # Initialize the historical state structure
    start_account_dict[ticker] = {
        "amount": 0,
        "initial price": 0,
        "current price": 0,
        "stock value in Portfolio": 0,
        "Price Change": 0,
        "percentage change": 0,
        "percentage portfolio": 0
    }

    # Gather all relevant transactions up to this date
    relevant_buys = create_relevant_buy_dict(ticker, start_date, tickers_buy_dict)
    relevant_sells = create_relevant_sell_dict(ticker, start_date, tickers_sell_dict)

    # Calculate net shares held at that point in time
    start_account_dict[ticker]["amount"] = sum(relevant_buys) - sum(relevant_sells)

    # Lookback logic: Find the last valid closing price if the market was closed on start_date
    attempts = 0
    search_date = start_date
    while True:
        try:
            if attempts > 9:  # Limit search to 10 days back
                start_account_dict[ticker]["current price"] = 0
                break

            # Attempt to fetch the closing price for the specific date
            price_data = find_prices(ticker, search_date.strftime("%Y-%m-%d"))
            start_account_dict[ticker]["current price"] = bring_price(price_data, 'close')
            break
        except Exception:
            attempts += 1
            search_date -= timedelta(days=1)

            # Finalize state metrics
    current_shares = start_account_dict[ticker]["amount"]
    closing_price = start_account_dict[ticker]["current price"]

    start_account_dict[ticker]["stock value in Portfolio"] = current_shares * closing_price

    # Set the 'initial price' base for the upcoming simulation period
    if current_shares != 0:
        start_account_dict[ticker]["initial price"] = closing_price
    else:
        start_account_dict[ticker]["initial price"] = 0

    return start_account_dict
def update_dict_ticker_num(ticker: str, tickers_dict: dict) -> int:
    """
    Determines the next transaction sequence number for a specific ticker.

    Args:
        ticker (str): The stock ticker symbol.
        tickers_dict (dict): The dictionary containing transaction history for tickers.

    Returns:
        int: The next available transaction number (starts at 1).
    """
    # Retrieve the existing list of numbers or an empty list if not found
    num_list = tickers_dict[ticker].get("num", [])

    # Return 1 if the list is empty, otherwise increment the last number
    return num_list[-1] + 1 if num_list else 1
def update_dict_ticker(ticker: str, num: int, amount: int, stock_price: float,
                       buy_sell_date: str, tickers_dict: dict) -> None:
    """
    Appends a new set of trade data to the ticker's history in the dictionary.

    Args:
        ticker (str): The stock ticker symbol.
        num (int): The transaction sequence number.
        amount (int): The quantity of shares.
        stock_price (float): The price per share.
        buy_sell_date (str): The transaction date in 'YYYY-MM-DD' format.
        tickers_dict (dict): The dictionary where data is stored.
    """
    # Append values to their respective lists within the ticker's entry
    tickers_dict[ticker]["num"].append(num)
    tickers_dict[ticker]["amount"].append(amount)
    tickers_dict[ticker]["price"].append(stock_price)
    tickers_dict[ticker]["date"].append(buy_sell_date)

    return None
def bring_price(price_list: list, order_type: str) -> float:
    """
    Extracts a specific price point from a price data list based on the requested order.

    The input list is expected to follow the OHLCV structure:
    [Open, High, Low, Close, Volume].

    Args:
        price_list (list): A list containing price and volume data.
        order_type (str): The type of price to return ('open', 'high', 'low', 'close', 'volume').

    Returns:
        float: The requested price or volume value.

    Raises:
        ValueError: If an invalid order_type is provided.
    """
    # Mapping table for much cleaner and faster lookups compared to multiple IFs
    index_map = {
        "open": 0,
        "high": 1,
        "low": 2,
        "close": 3,
        "volume": 4
    }

    try:
        index = index_map[order_type.lower()]
        return price_list[index]
    except (KeyError, IndexError):
        raise ValueError(f"Invalid order type or data list: {order_type}")
def round_numeric_values(data: dict, precision: int = 3) -> dict:
    """
    Recursively rounds all numeric values (float, np.float64) in a nested dictionary.

    Args:
        data (dict): The nested dictionary containing stock data.
        precision (int): Number of decimal places to round to. Defaults to 3.

    Returns:
        dict: The dictionary with all applicable values rounded.
    """
    for outer_key, inner_dict in data.items():
        for key, value in inner_dict.items():
            # Check for both standard Python floats and NumPy floats
            if isinstance(value, (float, np.float64)):
                inner_dict[key] = round(float(value), precision)

    return data
def make_account_table(data: dict) -> None:
    """
    Standardizes portfolio data and prints a formatted table to the terminal.

    Determines if the input data represents an 'Account' summary or a 'Profit' summary
    by analyzing the keys, then applies formatting via the tabulate library.

    Args:
        data (dict): Nested dictionary containing portfolio or profit data.

    Raises:
        ValueError: If the dictionary keys do not match expected account or profit structures.
    """
    # Define expected key sets for validation
    profit_keys = {
        'initial amount', 'final amount', 'initial price', 'final price',
        'initial stock value in Portfolio', 'final stock value in Portfolio',
        'profit', 'percentage change', 'percentage in portfolio'
    }
    account_keys = {
        'amount', 'initial price', 'stock value in portfolio',
        'price change', 'percentage change', 'percentage portfolio', 'current price'
    }

    # Identify the type of data by looking at the 'total' entry keys
    if "total" not in data:
        raise ValueError("Data dictionary must contain a 'total' entry for validation.")

    current_keys = set(data["total"].keys())

    # Case 1: Account Portfolio Table
    if current_keys == account_keys:
        refresh_current_price_in_account_dict(data)
        # Apply rounding once after the price refresh
        data = round_numeric_values(data)

        # Create DataFrame and format
        table = pd.DataFrame.from_dict(data, orient='index')
        formatted_table = tabulate(
            table,
            headers='keys',
            tablefmt='grid',
            numalign='center',
            stralign='center'
        )
        print(f"\n[ACCOUNT PORTFOLIO INFO]\n{formatted_table}")

    # Case 2: Profit/Historical Performance Table
    elif current_keys == profit_keys:
        data = round_numeric_values(data)
        table = pd.DataFrame.from_dict(data, orient="index")

        table.index.name = "Ticker"
        table.reset_index(inplace=True)

        # Rename columns for professional presentation
        table.columns = [
            "Ticker", "Init Amt", "Final Amt", "Init Price",
            "Final Price", "Init Value", "Final Value", "Profit ($)",
            "Change (%)", "Portfolio (%)"
        ]

        formatted_table = tabulate(
            table,
            headers="keys",
            tablefmt="fancy_grid",
            numalign="right",
            stralign="center",
            showindex=False
        )
        print(f"\n[PROFIT ANALYSIS REPORT]\n{formatted_table}")

    else:
        raise ValueError(f"Invalid data structure. Keys found: {current_keys}")
def refresh_current_price_in_account_dict(account_dict: dict) -> None:
    """
    Updates the 'current price' for all stocks in the dictionary using real-time data.

    Args:
        account_dict (dict): Portfolio dictionary where keys are tickers.
    """
    for ticker in account_dict:
        # Skip the summary row
        if ticker.lower() == 'total':
            continue

        new_price = get_current_price(ticker)
        if new_price is not None:
            account_dict[ticker]["current price"] = new_price
def make_order_table(data: dict) -> str:
    """
    Creates a formatted ASCII table from a dictionary of order data.

    Transposes the dictionary (where keys are headers and values are lists)
    into a row-based format suitable for tabular display.

    Args:
        data (dict): Dictionary with column names as keys and data lists as values.

    Returns:
        str: A string containing the formatted table.
    """
    if not data or not any(data.values()):
        return "No order data available."

    # Create a DataFrame and transpose to align data into columns
    table_df = pd.DataFrame.from_dict(data, orient="index").T

    # Generate the formatted table using a clean grid style
    formatted_table = tabulate(
        table_df,
        headers="keys",
        tablefmt="grid",
        numalign="center",
        stralign="center",
        showindex=False
    )

    return formatted_table
def super_update(tickers_dict: dict, ticker: str, amount: int,
                 price_per_stock: float = None, date: str = None) -> None:
    """
    Orchestrates the update of a ticker's transaction history.

    This function handles the logic of determining the transaction number,
    fetching market prices if not provided, and standardizing the date
    before committing the update to the dictionary.

    Args:
        tickers_dict (dict): The dictionary storing transaction history.
        ticker (str): The stock ticker symbol.
        amount (int): Number of shares in the transaction.
        price_per_stock (float, optional): Price per share. If None,
                                           fetches the closing price for the date.
        date (str, optional): Transaction date ('YYYY-MM-DD'). Defaults to today.
    """
    # 1. Get the next transaction sequence number
    num = update_dict_ticker_num(ticker, tickers_dict)

    # 2. Normalize the date (use current date if None)
    if date is None:
        date = now_date()

    # 3. Fetch price if not explicitly provided
    if price_per_stock is None:
        price_data = find_prices(ticker, date)
        price_per_stock = bring_price(price_data, "close")

    # 4. Perform a single update call with the prepared data
    update_dict_ticker(ticker, num, amount, price_per_stock, date, tickers_dict)
def show_order_info(tickers_dict: dict, order_type: str) -> None:
    """
    Iterates through all tickers and prints their detailed transaction history.

    Args:
        tickers_dict (dict): Dictionary containing the history of orders.
        order_type (str): Type of info to display ('buy' or 'sell').

    Raises:
        ValueError: If an invalid order_type is provided.
    """
    # Validate and set header title
    if order_type.lower() == "buy":
        print("\n[HISTORICAL BUYING ACTIVITY]")
    elif order_type.lower() == "sell":
        print("\n[HISTORICAL SELLING ACTIVITY]")
    else:
        raise ValueError(f"Invalid order_type: {order_type}. Use 'buy' or 'sell'.")

    print("=" * 30)

    # Display a table for each ticker in the history
    for ticker, history in tickers_dict.items():
        print(f"\nTicker: {ticker.upper()}")

        # Prepare the data structure for the table maker
        table_data = {
            "ID": history["num"],
            "Amount": history["amount"],
            "Price ($)": history["price"],
            "Date": history["date"],
        }

        # Render and print the table
        print(make_order_table(table_data))
def get_current_price(ticker_symbol: str) -> float | None:
    """
    Fetches the real-time market price of a stock using yfinance.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
        float | None: The last market price if successful, None if 'total' is passed.

    Raises:
        ValueError: If price data cannot be retrieved or the ticker is invalid.
    """
    if ticker_symbol.lower() == "total":
        return None

    try:
        stock = yf.Ticker(ticker_symbol)
        # fast_info provides low-latency access to the last price
        current_price = stock.fast_info["last_price"]

        if current_price is None:
            raise ValueError(f"No price data found for {ticker_symbol}")

        return float(current_price)
    except Exception as e:
        raise ValueError(f"Could not retrieve price for '{ticker_symbol}': {e}")
def update_account_dict(order_type_buy: bool, ticker: str, account_dict: dict,
                        sell_dict: dict = None, buy_dict: dict = None) -> dict:
    """
    Updates the portfolio state based on a Buy or Sell transaction.

    Recalculates share amounts, weighted average initial prices (for buys),
    and current market value/performance metrics.

    Args:
        order_type_buy (bool): True for a Buy order, False for a Sell order.
        ticker (str): The stock ticker symbol.
        account_dict (dict): The portfolio state to be updated.
        sell_dict (dict, optional): Transaction history for sells.
        buy_dict (dict, optional): Transaction history for buys.

    Returns:
        dict: The updated account_dict.

    Raises:
        ValueError: If required transaction dictionaries are missing or
                    if trying to sell more shares than owned.
    """
    if sell_dict is None and buy_dict is None:
        raise ValueError("Transaction data (buy_dict or sell_dict) must be provided.")

    ticker = ticker.upper()
    current_market_price = get_current_price(ticker)

    # --- CASE 1: BUY ORDER ---
    if order_type_buy:
        new_shares = buy_dict[ticker]["amount"][-1]
        new_buy_price = buy_dict[ticker]["price"][-1]

        if ticker not in account_dict:
            # Initialize new ticker entry
            account_dict[ticker] = {
                "amount": new_shares,
                "initial price": new_buy_price
            }
        else:
            # Update existing ticker using Weighted Average Price
            old_shares = account_dict[ticker]["amount"]
            old_initial_price = account_dict[ticker]["initial price"]

            total_shares = old_shares + new_shares
            weighted_avg_price = ((old_initial_price * old_shares) + (new_buy_price * new_shares)) / total_shares

            account_dict[ticker]["amount"] = total_shares
            account_dict[ticker]["initial price"] = weighted_avg_price

    # --- CASE 2: SELL ORDER ---
    else:
        shares_to_sell = sell_dict[ticker]["amount"][-1]
        current_shares = account_dict[ticker]["amount"]
        remaining_shares = current_shares - shares_to_sell

        if remaining_shares < 0:
            raise ValueError(f"Insufficient shares to sell {shares_to_sell} of {ticker}.")

        if remaining_shares == 0:
            del account_dict[ticker]
        else:
            account_dict[ticker]["amount"] = remaining_shares

    # --- POST-TRANSACTION RECALCULATION ---
    # If the ticker still exists in the portfolio, update its performance metrics
    if ticker in account_dict:
        data = account_dict[ticker]
        amt = data["amount"]
        init_p = data["initial price"]

        data["current price"] = current_market_price
        data["stock value in portfolio"] = amt * current_market_price
        data["price change"] = (current_market_price - init_p) * amt
        data["percentage change"] = ((current_market_price - init_p) / init_p) * 100

    # Refresh portfolio-wide weights
    update_percentage_portfolio(account_dict)

    return account_dict
def update_percentage_portfolio(account_dict: dict) -> None:
    """
    Calculates the weight of each stock relative to the total portfolio value.

    Args:
        account_dict (dict): The portfolio dictionary to update.
    """
    total_val = calculate_sum_portfolio(account_dict)

    if total_val == 0:
        return

    for ticker, info in account_dict.items():
        if ticker.lower() == 'total':
            continue
        # Calculate percentage (0-100)
        info["percentage portfolio"] = (info["stock value in portfolio"] / total_val) * 100
def calculate_sum_portfolio(account_dict: dict) -> float:
    """
    Calculates the aggregate market value of the entire portfolio.

    Iterates through all tickers and sums their 'stock value in portfolio'.
    Automatically skips the 'total' summary row to prevent double-counting.

    Args:
        account_dict (dict): Dictionary containing portfolio assets.

    Returns:
        float: The total market value of the portfolio.
    """
    # Use a generator expression with sum() for better performance and readability
    return sum(
        info["stock value in portfolio"]
        for ticker, info in account_dict.items()
        if ticker.lower() != "total"
    )
def create_account_sum(account_dict: dict) -> None:
    """
    Generates a 'total' summary entry in the account dictionary.

    Aggregates metrics across all holdings, including total shares,
    weighted average prices, total P&L, and overall portfolio percentage.

    Args:
        account_dict (dict): The portfolio dictionary to be modified in-place.
    """
    # 1. Aggregate fundamental metrics
    total_shares = calculate_total_amount_of_stock(account_dict)
    avg_init_price = calculate_average_initial_price(account_dict)
    total_market_value = calculate_total_value_in_portfolio(account_dict)
    total_pl_abs = calculate_total_price_change(account_dict)

    # 2. Calculate derivative metrics with safety checks
    overall_perc_change = calculate_percentage_change(
        avg_init_price, total_shares, total_market_value
    )
    avg_curr_price = calculate_average_current_price(total_market_value, total_shares)

    # 3. Commit the summary row
    account_dict["total"] = {
        "amount": total_shares,
        "initial price": avg_init_price,
        "current price": avg_curr_price,
        "stock value in portfolio": total_market_value,
        "price change": total_pl_abs,
        "percentage change": overall_perc_change,
        "percentage portfolio": 100.0  # Total portfolio is always 100% of itself
    }
def calculate_average_current_price(total_market_value: float, total_shares: int) -> float:
    """
    Calculates the volume-weighted average current price of the portfolio.

    Args:
        total_market_value (float): Sum of all stock values.
        total_shares (int): Sum of all shares owned.

    Returns:
        float: The weighted average price, or 0.0 if no shares are owned.
    """
    if total_shares == 0:
        return 0.0

    return total_market_value / total_shares
def calculate_percentage_change(average_initial_price: float, total_amount_of_stock: int,
                                total_value_in_portfolio: float) -> float:
    """
    Calculates the overall percentage return (ROI) for the entire portfolio.

    Args:
        average_initial_price (float): The weighted average entry price of all stocks.
        total_amount_of_stock (int): The total quantity of all shares held.
        total_value_in_portfolio (float): The current aggregate market value.

    Returns:
        float: The percentage change (0-100). Returns 0.0 if the initial cost basis is zero.
    """
    # Calculate the total cost basis
    cost_basis = average_initial_price * total_amount_of_stock

    # Safety check: Prevent division by zero if the portfolio is empty or cost is zero
    if cost_basis == 0:
        return 0.0

    # ROI Formula: ((Current Value - Cost Basis) / Cost Basis) * 100
    percentage_change = (total_value_in_portfolio - cost_basis) * 100 / cost_basis
    return percentage_change
def calculate_total_price_change(account_dict: dict) -> float:
    """
    Sums the absolute price change (profit/loss in currency) across all portfolio holdings.

    Args:
        account_dict (dict): Dictionary containing portfolio assets.

    Returns:
        float: Total absolute price change.
    """
    total_change = 0
    for ticker, info in account_dict.items():
        # CRITICAL: Skip the summary row to avoid double-counting the total
        if ticker.lower() == "total":
            continue
        total_change += info.get("price change", 0)

    return total_change
def calculate_total_value_in_portfolio(account_dict: dict) -> float:
    """
    Sums the current market value of all stocks currently held in the portfolio.

    Args:
        account_dict (dict): Dictionary containing portfolio assets.

    Returns:
        float: Total aggregate portfolio value.
    """
    total_val = 0
    for ticker, info in account_dict.items():
        # CRITICAL: Skip the summary row to avoid double-counting the total
        if ticker.lower() == "total":
            continue
        total_val += info.get("stock value in portfolio", 0)

    return total_val
def calculate_average_initial_price(account_dict: dict) -> float:
    """
    Calculates the volume-weighted average initial purchase price for the entire portfolio.

    The average is computed by summing the (initial price * shares) for every holding
    and dividing by the total number of shares in the portfolio.

    Args:
        account_dict (dict): The portfolio dictionary.

    Returns:
        float: The weighted average initial price, or 0.0 if no shares are held.
    """
    total_cost_basis = 0

    # Calculate total shares using the helper function
    total_shares = calculate_total_amount_of_stock(account_dict)

    # Safety check: Prevent division by zero
    if total_shares == 0:
        return 0.0

    for ticker, info in account_dict.items():
        # Skip the summary row to avoid double-counting
        if ticker.lower() == "total":
            continue

        # Add (price * amount) to the total cost basis
        shares = info.get("amount", 0)
        price = info.get("initial price", 0)
        total_cost_basis += shares * price

    return total_cost_basis / total_shares
def calculate_total_amount_of_stock(account_dict: dict) -> int:
    """
    Calculates the aggregate number of all shares held across all tickers.

    Args:
        account_dict (dict): The portfolio dictionary.

    Returns:
        int: Total number of shares.
    """
    total_shares = 0
    for ticker, info in account_dict.items():
        # Skip the summary row to avoid double-counting
        if ticker.lower() == "total":
            continue
        total_shares += info.get("amount", 0)

    return total_shares
def calculate_total_amount_of_stock_profit(profit_dict: dict) -> tuple:
    """
    Calculates the total share count at both the start and end of a profit report period.

    Args:
        profit_dict (dict): Dictionary containing historical profit metrics.

    Returns:
        tuple: A tuple containing (total_initial_shares, total_final_shares).
    """
    total_initial: int = 0
    total_final: int = 0

    for ticker, metrics in profit_dict.items():
        # Skip summary if present
        if ticker.lower() == "total":
            continue

        total_initial += metrics.get("initial amount", 0)
        total_final += metrics.get("final amount", 0)

    return (total_initial, total_final)
def calculate_total_value_in_portfolio_profit(profit_dict: dict) -> tuple:
    """
    Calculates total aggregate initial and final market values from a profit report.

    Args:
        profit_dict (dict): Dictionary containing historical profit metrics.

    Returns:
        tuple: (total_initial_market_value, total_final_market_value)
    """
    total_initial: float = 0
    total_final: float = 0

    for ticker, metrics in profit_dict.items():
        if ticker.lower() == "total":
            continue

        # Consistent key access using .get() to avoid KeyErrors
        total_initial += metrics.get("initial stock value in Portfolio", 0)
        total_final += metrics.get("final stock value in Portfolio", 0)

    return total_initial, total_final
def calculate_average_price_of_stock_profit(profit_dict: dict,
                                            total_init_amt: int,
                                            total_final_amt: int) -> tuple:
    """
    Calculates weighted average initial and final stock prices for the report period.

    Args:
        profit_dict (dict): Dictionary with ticker-specific profit data.
        total_init_amt (int): Sum of all initial share amounts.
        total_final_amt (int): Sum of all final share amounts.

    Returns:
        tuple: (weighted_avg_initial_price, weighted_avg_final_price)
    """
    sum_initial_cost: float = 0
    sum_final_value: float = 0

    for ticker, metrics in profit_dict.items():
        if ticker.lower() == "total":
            continue

        sum_initial_cost += metrics["initial amount"] * metrics["initial price"]
        sum_final_value += metrics["final amount"] * metrics["final price"]

    # Calculate average initial price with safety check
    avg_initial = sum_initial_cost / total_init_amt if total_init_amt > 0 else 0.0

    # Calculate average final price with safety check
    avg_final = sum_final_value / total_final_amt if total_final_amt > 0 else 0.0

    return avg_initial, avg_final
def calculate_profit_sum(profit_dict: dict) -> float:
    """
    Calculates the total net profit/loss across all tickers in the report.

    Args:
        profit_dict (dict): Dictionary containing profit data.

    Returns:
        float: Total absolute profit.
    """
    total_profit: float = 0
    for ticker, metrics in profit_dict.items():
        if ticker.lower() == "total":
            continue
        total_profit += metrics.get("profit", 0)

    return total_profit
def calculate_percentage_change_profit(profit_dict: dict) -> float:
    """
    Calculates the total weighted percentage change for the portfolio.

    The calculation follows the formula:
    """
    # Equation for Weighted Average Percentage Change:
    # $$ \text{Total \% Change} = \sum_{i=1}^{n} (\text{Ticker \% Change}_i \times \text{Weight in Portfolio}_i) $$

    total_percentage_change: float = 0
    for ticker, metrics in profit_dict.items():
        if ticker.lower() == "total":
            continue

        change = metrics.get("percentage change", 0)
        weight = metrics.get("percentage in portfolio", 0)
        total_percentage_change += (change * weight) / 100

    return total_percentage_change
def update_percentage_in_portfolio(profit_dict: dict, total_final_value: float) -> dict:
    """
    Updates the weight of each stock relative to the total portfolio value at the end date.

    Args:
        profit_dict (dict): Dictionary containing profit data.
        total_final_value (float): The aggregate final market value of the portfolio.

    Returns:
        dict: The updated profit_dict with weights assigned.
    """
    if total_final_value == 0:
        for ticker in profit_dict:
            profit_dict[ticker]["percentage in portfolio"] = 0
        return profit_dict

    for ticker in profit_dict:
        if ticker.lower() == "total":
            continue
        final_val = profit_dict[ticker]["final stock value in Portfolio"]
        profit_dict[ticker]["percentage in portfolio"] = (final_val / total_final_value) * 100

    return profit_dict
def create_all_profit_dict(profit_dict: dict) -> dict:
    """
    Aggregates all performance metrics into a 'total' summary row for the profit report.
    """
    # 1. Fetch aggregate metrics using helper functions
    amounts = calculate_total_amount_of_stock_profit(profit_dict)
    prices = calculate_average_price_of_stock_profit(profit_dict, amounts[0], amounts[1])
    values = calculate_total_value_in_portfolio_profit(profit_dict)
    total_profit = calculate_profit_sum(profit_dict)

    # 2. Update weights and calculate total percentage change
    profit_dict = update_percentage_in_portfolio(profit_dict, values[1])
    total_perc_change = calculate_percentage_change_profit(profit_dict)

    # 3. Commit the summary 'total' row
    profit_dict["total"] = {
        "initial amount": amounts[0],
        "final amount": amounts[1],
        "initial price": prices[0],
        "final price": prices[1],
        "initial stock value in Portfolio": values[0],
        "final stock value in Portfolio": values[1],
        "profit": total_profit,
        "percentage change": total_perc_change,
        "percentage in portfolio": 100.0
    }

    return profit_dict

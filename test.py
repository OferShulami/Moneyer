import calculate_func
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import pandas_market_calendars as mcal


# Sample dictionary

buy_dict = {
    "AAPL": {
        "num": [1, 2, 3],
        "price": [150, 155, 160],
        "date": ["2024-12-01", "2023-11-15", "2024-01-10"]
    },
    "GOOG": {
        "num": [1, 2],
        "price": [2800, 2850],
        "date": ["2024-06-15", "2023-07-01"]
    }
}



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



# Sorting the dictionary by date
def sort_buy_dict_by_date_with_reset_num(buy_dict):
    sorted_dict = {}
    for ticker, data in buy_dict.items():
        # Combine the related lists (num, price, date) into tuples
        combined = list(zip(data["num"], data["price"], data["date"]))

        # Sort the tuples by the date (converted to datetime objects)
        sorted_combined = sorted(combined, key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"))

        # Unpack the sorted tuples back into separate lists
        _, sorted_price, sorted_date = zip(*sorted_combined)

        # Reset "num" to a sequential list starting from 1
        sorted_num = list(range(1, len(sorted_price) + 1))

        # Update the dictionary with the sorted and reset values
        sorted_dict[ticker] = {
            "num": sorted_num,
            "price": list(sorted_price),
            "date": list(sorted_date)
        }

    return sorted_dict

# Sort the dictionary
sorted_buy_dict = sort_buy_dict_by_date_with_reset_num(buy_dict)

# Print the sorted dictionary
print(make_order_table(sorted_buy_dict))
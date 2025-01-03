import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import pandas_market_calendars as mcal

import yfinance as yf
from datetime import datetime

def get_voo_price_on(date_str):
    """
    Fetch the price of VOO on a specific date.
    
    Args:
        date_str (str): Date in the format "YYYY-MM-DD" (e.g., "2024-04-12").
    
    Returns:
        float: Closing price of VOO on the given date, or None if not available.
    """
    # Parse the input date
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    # Download historical data for VOO
    voo = yf.Ticker("VOO")
    historical_data = voo.history(start=target_date, end=target_date + timedelta(days=1))
    
    # Check if data exists for the given date
    if not historical_data.empty:
        # Get the closing price
        closing_price = historical_data.iloc[0]["Close"]
        return closing_price
    else:
        return None

# Example Usage
date = "2024-12-04"
price = get_voo_price_on(date)
if price:
    print(f"The price of VOO on {date} was ${price:.2f}")
else:
    print(f"No data available for VOO on {date}.")


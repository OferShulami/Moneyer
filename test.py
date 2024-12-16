import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import pandas_market_calendars as mcal


end_date = datetime.strptime("2022-10-10", "%Y-%m-%d")
print(type(end_date))
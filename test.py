import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import pandas_market_calendars as mcal



time = datetime(2022,11,1)
time = time - 1
print(time)
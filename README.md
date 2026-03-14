# Stock Portfolio Management & Analytics Engine 📈

A sophisticated financial tool designed to manage stock market trades, calculate real-time portfolio performance, and analyze historical profit/loss data using the Yahoo Finance API.

## Overview
This project consists of a high-level `Account` management system and a powerful calculation engine. It transforms raw transaction data into a live financial dashboard, handling complex scenarios like weighted average costs, market holidays, and historical performance tracking.

## Core Features
* **Real-Time Data Integration:** Fetches live market data (Open, High, Low, Close, Volume) using the `yfinance` library.
* **Automated Trade Ledger:** Tracks every buy and sell order, ensuring data integrity with automatic ticker validation.
* **Smart Market Calendar:** Utilizes `pandas_market_calendars` to validate trade dates against the NASDAQ schedule, automatically adjusting for weekends and holidays.
* **Advanced Financial Logic:**
    * **Weighted Average Cost:** Recalculates initial price per share after multiple buy-ins.
    * **Live Portfolio Metrics:** Calculates total value, absolute price change, and percentage distribution across the portfolio.
    * **Historical Profit Analysis:** A dedicated algorithm that reconstructs a "timeline" of trades to calculate realized and unrealized gains over specific timeframes.
* **Professional Reporting:** Generates clean, formatted summary tables directly in the terminal using `pandas` and `tabulate`.

## Project Structure
* **`Account.py`**: The main class interface. Handles user interactions, trade recording, and high-level reporting logic.
* **`calculate_func.py`**: The analytical core. Contains the mathematical functions, date sanitization logic, and API wrappers.

## Installation

### Prerequisites
* Python 3.x
* A Mac/PC with internet access (for API calls)

### Setup
1. Clone the repository.
2. Install the necessary libraries:
   ```bash
   pip install yfinance pandas tabulate pandas-market-calendars numpy

# Moneyer: Stock Portfolio Management & Analytics Engine 💰📈

A professional Python-based financial tool designed to manage stock market trades, calculate real-time portfolio performance, and analyze historical profit/loss data using the Yahoo Finance API.

## 🌟 Overview
Moneyer transforms raw transaction data into a live financial dashboard. It handles complex financial scenarios like weighted average costs, market holidays, and historical performance tracking, providing a clear view of your investment's health.

## 🚀 Core Features
* **Real-Time Data Integration:** Fetches live market data (Open, High, Low, Close, Volume) using the `yfinance` library.
* **Smart Market Calendar:** Utilizes `pandas_market_calendars` to validate trade dates against the NASDAQ schedule, automatically adjusting for weekends and holidays.
* **Advanced Financial Logic:**
    * **Weighted Average Cost (WAC):** Automatically recalculates the average price per share across multiple buy-ins.
    * **Time-Bound Profit Analysis:** A custom algorithm that calculates realized and unrealized gains over specific timeframes (ROI).
* **Professional Reporting:** Generates clean, color-coded summary tables in the terminal using `tabulate` and `colorama`.

## 📁 Project Structure
* **`user.py`**: The main interface. Contains the `Account` class, handles user interactions, and manages the portfolio state.
* **`calculate_func.py`**: The analytical core. Contains mathematical functions, date sanitization, and API wrappers.
* **`front_end.py`**: A CLI-based menu system for a seamless user experience.

## 🛠 Installation

### Prerequisites
* Python 3.x
* Internet connection (for real-time API calls)

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/OferShulami/Moneyer.git](https://github.com/OferShulami/Moneyer.git)

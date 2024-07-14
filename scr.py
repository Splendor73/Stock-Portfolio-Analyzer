import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Function to scrape DJIA stocks from Wikipedia
def scrape_djia_stocks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    rows = table.findAll('tr')[1:]  # Skip header row
    stocks = []
    for row in rows:
        cols = row.findAll('td')
        stock_symbol = cols[1].text.strip()  # Assuming stock symbol is in the second column
        industry = cols[2].text.strip()  # Assuming industry is in the fourth column
        stocks.append((stock_symbol, industry))
    return stocks

# Function to get stock data from Alpha Vantage
def get_stock_data(symbol, rapidapi_key):
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {
        "symbol": symbol,
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "datatype": "json"
    }
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        if "Monthly Adjusted Time Series" in data:
            # Extract the "Monthly Adjusted Time Series" data
            time_series = data["Monthly Adjusted Time Series"]
            # Filter by date range (using full range for now)
            filtered_data = filter_date_range(time_series, "2020-01-01", "2023-01-01")
            return filtered_data
        else:
            print(f"Error in response for {symbol}: {data}")
            return None
    else:
        print(f"Failed to fetch data for {symbol}: {response.status_code}")
        return None

def filter_date_range(historical_data, start_str, end_str):
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")
    filtered_data = {}
    for date, data in historical_data.items():
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        if start_date <= date_obj <= end_date:
            filtered_data[date] = data
    return filtered_data

def prepare_stock_dataframe(stock_df, symbol, quantity):
    # Add additional columns for symbol and quantity
    stock_df['Symbol'] = symbol
    stock_df['Quantity'] = quantity
    return stock_df

def calculate_portfolio_metrics(all_stock_data, portfolio):
    # Ensure 'Date' is in datetime format and sort by Date
    all_stock_data['Date'] = pd.to_datetime(all_stock_data['Date'])
    all_stock_data.sort_values(by='Date', inplace=True)

    # Convert 'Adjusted Close' to numeric and calculate daily returns
    all_stock_data['Adjusted Close'] = pd.to_numeric(all_stock_data['5. adjusted close'], errors='coerce')
    all_stock_data['Daily Return'] = all_stock_data.groupby('Symbol')['Adjusted Close'].pct_change()

    # Calculate weighted returns based on the quantity of each stock
    all_stock_data['Weighted Return'] = all_stock_data['Daily Return'] * all_stock_data['Quantity']

    # Aggregate daily returns for the entire portfolio
    portfolio_returns = all_stock_data.groupby('Date')['Weighted Return'].sum()

    # Calculate portfolio metrics
    mean_daily_return = portfolio_returns.mean()
    std_dev_daily_returns = portfolio_returns.std()
    cumulative_returns = (1 + portfolio_returns).cumprod() - 1

    return mean_daily_return, std_dev_daily_returns, cumulative_returns.iloc[-1]

def fetch_and_prepare_data(portfolio, rapidapi_key):
    all_stock_data = pd.DataFrame()
    for symbol, quantity in portfolio.items():
        print(f"\nFetching data for {symbol}...")
        stock_data = get_stock_data(symbol, rapidapi_key)
        if stock_data:
            stock_df = pd.DataFrame.from_dict(stock_data, orient='index')
            stock_df = prepare_stock_dataframe(stock_df, symbol, quantity)
            all_stock_data = pd.concat([all_stock_data, stock_df])
        else:
            print(f"Failed to fetch data for {symbol}.")
    if all_stock_data.empty:
        return None
    all_stock_data.reset_index(inplace=True)
    all_stock_data.rename(columns={'index': 'Date'}, inplace=True)
    all_stock_data['Date'] = pd.to_datetime(all_stock_data['Date'])
    return all_stock_data

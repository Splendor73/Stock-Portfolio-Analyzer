import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pandas as pd
import time


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
def get_stock_data(symbol, rapidapi_key, start_date, end_date):
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
        # Extract the "Monthly Adjusted Time Series" data
        time_series = data.get("Monthly Adjusted Time Series", {})
        # Filter by date range
        filtered_data = filter_date_range(time_series, start_date, end_date)
        return filtered_data
    else:
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
    # Here you can also convert prices to numeric, if needed, and calculate returns
    # stock_df['Price'] = pd.to_numeric(stock_df['Price'], errors='coerce')
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


def main():

    # pd.set_option('display.max_rows', None) // uncomment this line if you want to see the full row of fetching data

    # Header
    print("=============================================")
    print("       DJIA Stock Portfolio Analysis")
    print("=============================================")

    wiki_url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    stocks = scrape_djia_stocks(wiki_url)
    if stocks:
        df = pd.DataFrame(stocks, columns=['Stock Symbol', 'Industry'])
        df.index += 1
        print("DJIA stock symbols and their industries:")
        print(df)
    else:
        print("Failed to scrape DJIA stocks.")
    
    # Your API key
    rapidapi_key = 'You Key'
    
    # Example format for user input: AAPL 5, BA 5
    print("Enter your stock portfolio using the format 'Symbol1 Quantity1, Symbol2 Quantity2,...' (e.g., 'AAPL 5, BA 5'):")
    portfolio_input = input("Your portfolio: ")
    portfolio_items = portfolio_input.split(",")  # Split input by commas to get individual stocks
    portfolio = {}
    for item in portfolio_items:
        symbol, quantity = item.strip().split()  # Split each item into symbol and quantity
        portfolio[symbol.upper()] = int(quantity)
    
    # Define date range
    start_date_str = '2020-01-01'
    end_date_str = '2023-01-01'

    # Initialize an empty DataFrame to hold all stock data
    all_stock_data = pd.DataFrame()

    # Fetch and organize stock data within the date range
    for symbol, quantity in portfolio.items():
        print(f"\nFetching data for {symbol}...")
        stock_data = get_stock_data(symbol, rapidapi_key, start_date_str, end_date_str)
        if stock_data:
            # Convert stock data to DataFrame
            stock_df = pd.DataFrame.from_dict(stock_data, orient='index')
            # Prepare and adjust the DataFrame
            stock_df = prepare_stock_dataframe(stock_df, symbol, quantity)
            # Concatenate the individual stock DataFrame to the all_stock_data DataFrame
            all_stock_data = pd.concat([all_stock_data, stock_df])
        else:
            print(f"Failed to fetch data for {symbol}.")

    # Once all data is fetched, reset the index and organize columns
    all_stock_data.reset_index(inplace=True)
    all_stock_data.rename(columns={'index': 'Date'}, inplace=True)
    # Ensure date is in datetime format
    all_stock_data['Date'] = pd.to_datetime(all_stock_data['Date'])

    # Print the compiled DataFrame
    print(all_stock_data)

    # At the end of your main() function, call the above method
    mean_daily_return, std_dev_daily_returns, cumulative_returns = calculate_portfolio_metrics(all_stock_data, portfolio)

    # Print the calculated metrics
    print(f"Mean Daily Return for the portfolio: {mean_daily_return:.6f}")
    print(f"Standard Deviation of Daily Returns for the portfolio: {std_dev_daily_returns:.6f}")
    print(f"Cumulative Returns of the portfolio: {cumulative_returns:.6f}")

if __name__ == "__main__":
    main()


```markdown
# DJIA Portfolio Analysis Tool

## Project Description
This Python-based tool is designed to automate the process of scraping Dow Jones Industrial Average (DJIA) stock symbols and their industries from Wikipedia. It integrates with the Alpha Vantage API to fetch historical stock data, enabling users to analyze their stock portfolio's performance. The tool calculates key portfolio metrics, such as mean daily return, standard deviation of daily returns, and cumulative returns.

## Installation

To get started with this project, you need to have Python installed on your system. Then, you can follow these steps to install the necessary libraries:

```bash
pip install requests beautifulsoup4 pandas
```

Note: You'll need an API key from Alpha Vantage to fetch stock data. Obtain your key by signing up at [Alpha Vantage](https://www.alphavantage.co/).

## Usage

To use this tool, follow these steps:

1. Clone the repository to your local machine.
2. Open the project in your preferred IDE or text editor.
3. Replace the `rapidapi_key` variable value with your Alpha Vantage API key.
4. Run the script:

```bash
python src.py
```

5. When prompted, enter your stock portfolio using the format 'Symbol1 Quantity1, Symbol2 Quantity2,...' (e.g., 'AAPL 5, BA 5').

The tool will then fetch the necessary data and display your portfolio's performance metrics.

## Contributing

Contributions to this project are welcome. To contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

```
Author : "Yashu Patel
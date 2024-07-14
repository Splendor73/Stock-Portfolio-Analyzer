from flask import Flask, render_template, request, jsonify
import scr
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        portfolio_input = data.get('portfolio')
        rapidapi_key = data.get('apiKey')
        start_date = data.get('startDate')
        end_date = data.get('endDate')

        app.logger.debug(f"Received data: {data}")

        portfolio = {}
        for item in portfolio_input.split(','):
            symbol, quantity = item.strip().split()
            portfolio[symbol.upper()] = int(quantity)

        all_stock_data = scr.fetch_and_prepare_data(portfolio, rapidapi_key, start_date, end_date)
        if all_stock_data is None:
            return jsonify({'error': 'Failed to fetch stock data for the given portfolio'})

        mean_daily_return, std_dev_daily_returns, cumulative_returns = scr.calculate_portfolio_metrics(all_stock_data, portfolio)

        return jsonify({
            'mean_daily_return': mean_daily_return,
            'std_dev_daily_returns': std_dev_daily_returns,
            'cumulative_returns': cumulative_returns
        })
    except Exception as e:
        app.logger.error(f"Error occurred: {e}", exc_info=True)
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import scr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    portfolio_input = data.get('portfolio')
    rapidapi_key = data.get('apiKey')
    

    portfolio = {}
    for item in portfolio_input.split(','):
        symbol, quantity = item.strip().split()
        portfolio[symbol.upper()] = int(quantity)

    all_stock_data = scr.fetch_and_prepare_data(portfolio, rapidapi_key)
    if all_stock_data is None:
        return jsonify({'error': 'Failed to fetch stock data for the given portfolio'})

    mean_daily_return, std_dev_daily_returns, cumulative_returns = scr.calculate_portfolio_metrics(all_stock_data, portfolio)

    return jsonify({
        'mean_daily_return': mean_daily_return,
        'std_dev_daily_returns': std_dev_daily_returns,
        'cumulative_returns': cumulative_returns
    })

if __name__ == '__main__':
    app.run(debug=True)

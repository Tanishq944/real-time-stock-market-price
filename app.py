import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = 'XAKF19M630QO3438'  # Replace with your Alpha Vantage API key

# Alpha Vantage API URL for real-time stock quote
ALPHA_VANTAGE_URL = 'https://www.alphavantage.co/query'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol')
    stock_data = None
    error = None
    try:
        # Alpha Vantage API call for real-time stock data (Global Quote)
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': API_KEY
        }
        response = requests.get(ALPHA_VANTAGE_URL, params=params)
        data = response.json()

        # Check if the API response contains the expected data
        if 'Global Quote' in data:
            stock_data = data['Global Quote']
            if stock_data['05. price'] == 'None':
                error = f"No data found for {symbol}"
        else:
            error = "Invalid stock symbol or unable to fetch data."

    except Exception as e:
        error = "An error occurred while fetching the stock data."

    # Return error or stock data as JSON
    if error:
        return jsonify({'error': error})

    # Extract relevant data from API response
    data = {
        'symbol': symbol,
        'price': stock_data['05. price'],
        'open': stock_data['02. open'],
        'high': stock_data['03. high'],
        'low': stock_data['04. low'],
        'volume': stock_data['06. volume'],
        'date': stock_data['07. latest trading day']
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

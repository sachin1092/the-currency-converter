#!venv/bin/python
import json
from flask import Flask, jsonify, abort, make_response, request, url_for
import urllib2


app = Flask(__name__, static_url_path='')

root_url = "http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv"

currencies = {'ARS': 'Argentine peso', 'AUD': 'Australian dollar', 'BSD': 'Bahamian dollar', 'BRL': 'Brazilian real', 'XOF': 'CFA franc (African Financial Community)', 'XPF': 'CFP franc (Pacific Financial Community)', 'CLP': 'Chilean peso', 'CNY': 'Chinese renminbi', 'COP': 'Colombian peso', 'HRK': 'Croatian kuna', 'CZK': 'Czech Republic koruna', 'DKK': 'Danish krone', 'XCD': 'East Caribbean dollar', 'EUR': 'European Euro', 'FJD': 'Fiji dollar', 'GHS': 'Ghanaian cedi', 'GTQ': 'Guatemalan quetzal', 'HNL': 'Honduran lempira', 'HKD': 'Hong Kong dollar', 'HUF': 'Hungarian forint', 'ISK': 'Icelandic krona', 'INR': 'Indian rupee', 'IDR': 'Indonesian rupiah', 'ILS': 'Israeli new shekel', 'JMD': 'Jamaican dollar', 'JPY': 'Japanese yen', 'MYR': 'Malaysian ringgit', 'MXN': 'Mexican peso', 'MAD': 'Moroccan dirham', 'MMK': 'Myanmar (Burma) kyat', 'ANG': 'Neth. Antilles florin', 'NZD': 'New Zealand dollar', 'NOK': 'Norwegian krone', 'PKR': 'Pakistan rupee', 'PAB': 'Panamanian balboa', 'PEN': 'Peruvian new sol', 'PLN': 'Polish zloty', 'RON': 'Romanian new leu', 'RUB': 'Russian rouble', 'RSD': 'Serbian dinar', 'SGD': 'Singapore dollar', 'ZAR': 'South African rand', 'KRW': 'South Korean won', 'LKR': 'Sri Lanka rupee', 'SEK': 'Swedish krona', 'CHF': 'Swiss franc', 'TWD': 'Taiwanese new dollar', 'THB': 'Thai baht', 'TTD': 'Trinidad and Tobago dollar', 'TND': 'Tunisian dinar', 'TRY': 'Turkish lira', 'AED': 'U.A.E. dirham', 'GBP': 'U.K. pound sterling', 'USD': 'U.S. dollar', 'CAD3': 'US/Canada noon 3-month forward points spread', 'CAD6': 'US/Canada noon 6-month forward points spread', 'VEF': 'Venezuelan bolivar fuerte', 'VND': 'Vietnamese dong'}

@app.route('/currency/v1.0/', methods=['GET'])
def get_all():
    return json.dumps(get_data())


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/currency/v1.0/<string:from_>/<string:to>/', methods=['GET'])
def get_specific(from_, to):
    return json.dumps(get_data(data_filter={'from_': from_, 'to': to}))


def get_data(data_filter={}):
    rates = {}

    try:
        date = "Unknown"

        fh = urllib2.urlopen(root_url)

        for line in fh:
            line = line.rstrip()
            if not line or line.startswith(("#", "Closing")):
                continue

            fields = line.split(",")
            if line.startswith("Date "):
                date = fields[-1]

            else:
                try:
                    value = float(fields[-1])
                    rates[str(fields[0]).strip()] = value
                except ValueError:
                    pass

        if len(data_filter):
            rate = (rates[currencies[data_filter['from_']]] / rates[currencies[data_filter['to']]])
            data = {'data': {'from': currencies[data_filter['from_']], 'from_short': data_filter['from_'], 'to': currencies[data_filter['to']], 'to_short': data_filter['to'], 'rate': rate}, 'date': str(date).strip()}
        else:
            data = {'data': rates, 'date': str(date).strip()}
        return data
    except Exception, e:
        print "Failed to download:\n%s" % e
        return {'data': {'error': e}}


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
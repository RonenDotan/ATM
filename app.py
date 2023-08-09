from flask import Flask, jsonify
from flask_restful import reqparse
from withdrawl_handler import withdraw
from refill_handler import refill


app = Flask(__name__)

@app.route('/')
def index():
    return 'ATM'

@app.route('/atm/withdrawl', methods=['POST'])
def withdrawl_endpoint():
    try: 
        parser = reqparse.RequestParser()
        parser.add_argument('amount', required=True, type=float, help='Must Specify amount to be withdrawn')
        args = parser.parse_args()
        amount = round(args['amount'], 2)
        result = withdraw(amount)
        return result, 200
    except Exception as e:
        return jsonify(
                data=e.message,
                status=e.status_code
            ), e.status_code

    
    


@app.route('/atm/refill', methods=['POST'])
def refill_endpoint():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('money', type=dict, help='Amount to be refilled')
        args = parser.parse_args()
        money = args['money']
        result = refill(money)
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(
                data=e.message,
                status=e.status_code
            ), e.status_code


@app.route('/atm/status', methods=['GET','POST'])
def status_endpoint():
    from atm_machine import atm
    return jsonify(atm.funds)

@app.route('/atm/test_db', methods=['GET','POST'])
def test_db_endpoint():
    return test()


def test():
    amount = 50
    return withdraw(amount)

    money = {"100" : 20, "10" : 5}
    result = refill(money)
    return jsonify(success=True)

# test()
if __name__ == '__main__':
    app.run(debug=True)
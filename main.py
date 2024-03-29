import braintree
import os
import sys
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(1, os.path.join(os.path.abspath("."), 'lib'))

from flask import Flask, request, render_template, url_for
app = Flask(__name__)

use_your_merchant_id = 'jfvb3db6n7cq67bw'
use_your_public_key = 'kgtgc7zrnbz2z2p5'
use_your_private_key = '5c7210241bd4bcd9393f7ef514313a6c'

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=use_your_merchant_id,
                                  public_key=use_your_public_key,
                                  private_key=use_your_private_key)


@app.route("/")
def form():
    return render_template("braintree.html")
    
@app.route("/client_token", methods=["GET"])
def client_token():
    return braintree.ClientToken.generate()

@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": request.form["number"],
            "cvv": request.form["cvv"],
            "expiration_month": request.form["month"],
            "expiration_year": request.form["year"]
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        return "<h1>Success! Transaction ID: {0}</h1>".format(result.transaction.id)
    else:
        return "<h1>Error: {0}</h1>".format(result.message)

#if __name__ == '__main__':
#    app.run(debug=True)

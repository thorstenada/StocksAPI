import flask
import pandas as pd
import json
from flask import request, jsonify, send_file
import cf_financial_analysis as cf

#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>CleverFinance API</h1>"
    
@app.route('/api/v1/cf_financial_analysis/ticker', methods=['GET'])
def api_id_json():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No ticker field provided. Please specify an ticker."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    results = cf.get_financial_analysis_df(id).to_json(orient="split")
    results = json.loads(results)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/v1/cf_financial_analysis/graph', methods=['GET'])
def api_id_graph():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No ticker field provided. Please specify an ticker."

    pid = cf.perform_technical_analysis(id, n=180)
    return send_file(pid, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#start application
app.run()




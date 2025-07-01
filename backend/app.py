from flask_cors import CORS
from flask import Flask, jsonify, abort
import pandas as pd
import os

app = Flask(__name__)

CORS(app, origins='*')

def load_data():
    """Loads data from the csv file"""
    try:
        df = pd.read_csv('./Table_Input.csv')
        df.rename(columns={'Index #': 'index'}, inplace=True)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []
    except Exception:
        return []

@app.route('/api', methods=['GET'])
def get_table():
    """getting the data and exposing it as an endpoint through the endpoint"""
    data = load_data()
    return jsonify(data)

@app.route('/api/values/<index>', methods=['GET'])
def get_value_by_index(index):
    """getting the value by its index"""
    data = load_data()
    filtered_data = [row for row in data if row['index'] == index]
    
    if not filtered_data:
        abort(404)
    
    return jsonify(filtered_data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
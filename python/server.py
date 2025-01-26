
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Endpoint for fetching subnets
@app.route('/fetch-subnets', methods=['POST'])
def fetch_subnets():
    try:
        # Extract API key and organization handle from the request
        data = request.json
        api_key = data.get('apiKey')
        org_handle = data.get('orgHandle')

        if not api_key or not org_handle:
            return jsonify({"error": "API Key and Organization Handle are required"}), 400

        # RIPE NCC API URL
        url = f"https://rest.db.ripe.net/search?source=ripe&query-string={org_handle}"
        headers = {"Authorization": f"ApiKey {api_key}"}

        # Make the request to RIPE NCC
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(
                {
                    'content': response.content.decode()
                }
            )
        else:
            return jsonify({"error": f"Failed to fetch subnets: {response.status_code}", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
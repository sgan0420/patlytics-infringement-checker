import json

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Test route
@app.route("/")
def home():
    return "Backend is working!"


# Endpoint to handle form submissions
@app.route("/api/infringement-check", methods=["POST"])
def infringement_check():
    # Get JSON data from the request
    data = request.json
    patent_id = data.get("patentId")
    company_name = data.get("companyName")

    # Example response
    response = {
        "message": "Data received successfully",
        "patentId": patent_id,
        "companyName": company_name,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)


# Load JSON files
with open("patents.json", encoding="utf-8") as patents_file:
    patents_data = json.load(patents_file)

with open("company_products.json", encoding="utf-8") as products_file:
    products_data = json.load(products_file)["companies"]


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

    # Find the patent by ID
    patent = next((p for p in patents_data if p["publication_number"] == patent_id), None)
    if not patent:
        return jsonify({"error": f"Patent ID '{patent_id}' not found"}), 404

    # Find the company by name
    company = next((c for c in products_data if c["name"].lower() == company_name.lower()), None)
    if not company:
        return jsonify({"error": f"Company '{company_name}' not found"}), 404

    # Response
    response = {
        "analysis_id": "1",
        "patent_id": patent_id,
        "company_name": company_name,
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_infringement_products": [],
        "overall_risk_assessment": "High",
        "patent": patent,
        "company": company,
    }

    return app.response_class(response=json.dumps(response, sort_keys=False), mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)

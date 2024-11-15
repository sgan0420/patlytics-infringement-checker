import json
import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


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


def analyze_infringement_with_openai(claims_text, product_text):
    try:
        response = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:patlytics-patent-test:ATlBDC1p",
            messages=[
                {
                    "role": "system",
                    "content": "You are a system designed to return JSON-encoded patent infringement analyses. Please strictly format your response as valid JSON without extra text or commentary.",
                },
                {
                    "role": "user",
                    "content": json.dumps({"claims": claims_text, "company_products": product_text}),
                },
            ],
        )
        gpt_response = response.choices[0].message.content
        return json.loads(gpt_response)
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")


def validate_analysis_result(result):
    required_keys = ["infringement_likelihood", "relevant_claims", "explanation", "specific_features"]
    if not isinstance(result, dict):
        return False
    for key in required_keys:
        if key not in result:
            return False
    return True


def analyze_each_product(claims_text, company_products):
    results = []
    for product in company_products:
        analysis_result = None
        attempts = 0
        max_attempts = 3  # Retry up to 3 times
        while attempts < max_attempts:
            try:
                analysis_result = analyze_infringement_with_openai(claims_text, product)
                if validate_analysis_result(analysis_result):
                    if analysis_result["infringement_likelihood"].lower() != "low":
                        results.append({"product_name": product["name"], "analysis_result": analysis_result})
                    break  # Valid result, exit attempt loop
            except RuntimeError as e:
                print(f"Error analyzing product '{product['name']}' (attempt {attempts + 1}): {e}")
            attempts += 1

        if attempts == max_attempts and not validate_analysis_result(analysis_result):
            return {"error": f"Failed to analyze product '{product['name']}' after {max_attempts} retries.", "product_name": product["name"]}

    return results


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

    claims_text = "\n".join([claim["text"] for claim in json.loads(patent["claims"])])
    company_products = company["products"]

    try:
        infringing_products = analyze_each_product(claims_text, company_products)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    # Response
    response = {
        "analysis_id": "1",
        "patent_id": patent_id,
        "company_name": company_name,
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_infriging_products": infringing_products,
    }

    return app.response_class(response=json.dumps(response, sort_keys=False), mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)

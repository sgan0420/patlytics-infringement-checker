import json
import os
import uuid
import re
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from fuzzywuzzy import process


api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")


app = Flask(__name__)
CORS(app)


with open("patents.json", encoding="utf-8") as patents_file:
    patents_data = json.load(patents_file)

with open("company_products.json", encoding="utf-8") as products_file:
    products_data = json.load(products_file)["companies"]


HISTORY_FILE = "analysis_history.json"


# Test route
@app.route("/")
def home():
    return "Backend is working!"


def load_analysis_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_analysis_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


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
        max_attempts = 3
        while attempts < max_attempts:
            try:
                analysis_result = analyze_infringement_with_openai(claims_text, product)
                if validate_analysis_result(analysis_result):
                    results.append(
                        {
                            "product_name": product["name"],
                            "infringement_likelihood": analysis_result["infringement_likelihood"],
                            "relevant_claims": analysis_result["relevant_claims"],
                            "explanation": analysis_result["explanation"],
                            "specific_features": analysis_result["specific_features"],
                        }
                    )
                    break
            except RuntimeError as e:
                print(f"Error analyzing product '{product['name']}' (attempt {attempts + 1}): {e}")
            attempts += 1

        if attempts == max_attempts and not validate_analysis_result(analysis_result):
            return jsonify({"error": f"Failed to analyze product '{product['name']}' after {max_attempts} retries."}), 500

    likelihood_order = {"High": 3, "Moderate": 2, "Low": 1}
    sorted_results = sorted(
        results,
        key=lambda x: (
            likelihood_order.get(x["infringement_likelihood"], 0),
            len(x["relevant_claims"]),
        ),
        reverse=True,
    )

    return sorted_results[:2] if len(sorted_results) >= 2 else sorted_results


def normalize_company_name(name):
    suffixes = ["inc.", "inc", "co.", "co", "corporation", "corporations", "corp.", "corp", "ltd", "limited", "llc", "llp"]
    normalized_name = name.lower()
    for suffix in suffixes:
        normalized_name = re.sub(r'\s*' + re.escape(suffix) + r'\s*$', '', normalized_name)
    return normalized_name


@app.route("/api/analyze-patent-infringement", methods=["POST"])
def analyze_patent_infringement():
    data = request.json
    patent_id = data.get("patentId")
    company_name = data.get("companyName")

    patent = next((p for p in patents_data if p["publication_number"].lower() == patent_id.lower()), None)
    if not patent:
        return jsonify({"error": f"Patent ID '{patent_id}' not found"}), 404

    normalized_company_name = normalize_company_name(company_name)
    all_company_names = [normalize_company_name(c["name"]) for c in products_data]
    best_match, score = process.extractOne(normalized_company_name, all_company_names)
    company = next((c for c in products_data if normalize_company_name(c["name"]) == best_match), None)
    if score < 95:
        return jsonify({"error": f"Company '{company_name}' not found. Did you mean '{company['name']}'?"}), 404

    claims_text = "\n".join([claim["text"] for claim in json.loads(patent["claims"])])
    company_products = company["products"]

    try:
        infringing_products = analyze_each_product(claims_text, company_products)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    analysis_id = str(uuid.uuid4())

    response = {
        "analysis_id": analysis_id,
        "patent_id": patent_id,
        "company_name": company["name"],
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_infringing_products": infringing_products,
    }

    return app.response_class(response=json.dumps(response, sort_keys=False), mimetype="application/json")


@app.route("/api/get-analysis-history", methods=["GET"])
def get_analysis_history():
    history = load_analysis_history()
    if not history:
        return jsonify({"message": "No analysis history found"})
    return app.response_class(response=json.dumps(history, sort_keys=False), mimetype="application/json")


@app.route("/api/save-analysis", methods=["POST"])
def save_analysis():
    history = load_analysis_history()

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    analysis_id = data.get("analysis_id")
    patent_id = data.get("patent_id")
    company_name = data.get("company_name")
    analysis_date = data.get("analysis_date")
    top_infringing_products = data.get("top_infringing_products")

    for existing_analysis in history:
        if existing_analysis["analysis_id"] == analysis_id:
            return jsonify({"error": "Analysis has already been saved."}), 400

    response = {
        "analysis_id": analysis_id,
        "patent_id": patent_id,
        "company_name": company_name,
        "analysis_date": analysis_date,
        "top_infringing_products": top_infringing_products,
    }

    history.append(response)
    save_analysis_history(history)

    return jsonify({"message": "Analysis saved successfully", "saved_analysis": response})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

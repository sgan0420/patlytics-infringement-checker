import json
import os

with open(os.path.join("..", "patents.json"), encoding="utf-8") as patents_file:
    patents_data = json.load(patents_file)

with open(os.path.join("..", "company_products.json"), encoding="utf-8") as products_file:
    products_data = json.load(products_file)["companies"]

with open("assistant_response.json", encoding="utf-8") as response_file:
    response_data = json.load(response_file)

with open("infringement_analysis.jsonl", "w", encoding="utf-8") as analysis_file:
    claims_text = "\n".join([claim["text"] for claim in json.loads(patents_data[0]["claims"])])
    for i in range(len(products_data[0]["products"])):
        product_text = products_data[0]["products"][i]
        response_text = response_data[i]
        jsonl_entry = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a system designed to return JSON-encoded patent infringement analyses. Please strictly format your response as valid JSON without extra text or commentary.",
                },
                {
                    "role": "user",
                    "content": "{claims: " + claims_text + "\ncompany_products: " + str(product_text) + "}",
                },
                {
                    "role": "assistant",
                    "content": str(response_text),
                },
            ]
        }
        analysis_file.write(json.dumps(jsonl_entry) + "\n")

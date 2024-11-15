import json
import os

with open(os.path.join("..", "patents.json"), encoding="utf-8") as patents_file:
    patents_data = json.load(patents_file)

with open(os.path.join("..", "company_products.json"), encoding="utf-8") as products_file:
    products_data = json.load(products_file)["companies"]

with open("infringement_analysis.jsonl", "w", encoding="utf-8") as analysis_file:
    products_list = products_data[0]["products"]
    for product in products_list:
        claims_text = []
        for claim in json.loads(patents_data[0]["claims"]):
            claims_text.append(claim["text"])
        print(claims_text)
        jsonl_entry = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a system designed to return JSON-encoded patent infringement analyses. Please strictly format your response as valid JSON without extra text or commentary.",
                },
                {
                    "role": "user",
                    "content": "{claims: " + str(claims_text) + ", company_products: " + str(product) + "}",
                },
                {
                    "role": "assistant",
                    "content": "",
                },
            ]
        }
        analysis_file.write(json.dumps(jsonl_entry) + "\n")

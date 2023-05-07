# -*- coding: utf-8 -*-
""" Extract samples from reference documentation """
import bs4 as bs
import json

json_examples = {}

# Extract the name, endpoint, and sample response for each API call
with open("references/rest_api_all_resources.html", "r") as f:
    soup = bs.BeautifulSoup(f.read(), "html.parser")
for resource in soup.find_all("div", class_="method_details"):
    try:
        name = resource.find("h2", class_="api_method_name").getText().strip()
        endpoint = resource.find("h3", class_="endpoint").getText().strip()
        response = resource.find("div", class_="examples example_response").find("pre").getText().strip()
        readable_json = ""
        for line in response.split("\n"):
            readable_json += line + "\n"
        response = readable_json
        json_examples[name] = {"endpoint": endpoint, "response": json.loads(response), "valid": True}
    except AttributeError:
        continue
    except json.decoder.JSONDecodeError:
        json_examples[name] = {"endpoint": endpoint, "response": response, "valid": False}

with open("sample_responses.json", "w") as f:
    json.dump(json_examples, f, indent=4, sort_keys=True)
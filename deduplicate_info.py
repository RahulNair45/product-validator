import json

file_name = "meal prep app_discourse.json"
cleaned_file_name = f"cleaned_{file_name}"

with open(file_name, "r") as f:
    results = json.load(f)

seen_urls = set()
unique_results = []

for result in results:
    if  result["title"] and result["url"] and result["text"]:
        result["title"] = result["title"].strip()
        result["url"] = result["url"].strip()
        result["text"] = result["text"].strip()
        if result["url"] not in seen_urls:
            seen_urls.add(result["url"])
            unique_results.append(result)


with open(cleaned_file_name, "w") as f:
    json.dump(unique_results, f, indent=2)
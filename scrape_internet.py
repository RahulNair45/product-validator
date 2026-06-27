import requests
import json

API_KEY = "BSAJLuYHcrha7OHCT67-oM5Ef4_X5Hn"

def search(query):
    url = "https://api.search.brave.com/res/v1/web/search" # braves end point (url api listens to for requests)

    headers = {
        "Accept": "application/json", # gives json back
        "Accept-Encoding": "gzip", # compresses the response for speed
        "X-Subscription-Token": API_KEY
    }

    params = {
        "q": query, # the search 
        "count": 10 # num or results given back
    }

    response = requests.get(url, headers=headers, params=params) # sends the requests
    data = response.json() # converts response to python dict

    # for result in data["web"]["results"]:  # loop through results
    #     print(result["title"])        # page title
    #     print(result["url"])          # page link
    #     print(result["description"])  # preview text
    #     print("---")
    
    return data

def generate_queries(product_idea):
    return [
        f"{product_idea} problems",           # pain & frustration from real people
        f"why is {product_idea} so hard",            # people actively struggling
        f"{product_idea} alternatives",              # people looking for something better
        f"I wish {product_idea} could",              # feature gaps and missing things
        f"is there an app that does {product_idea}", # people searching for a solution
        f"{product_idea} reviews complaints",        # competitor weaknesses
        f"would you pay for {product_idea}",         # market validation
    ]

def find_discourse(product_idea):

    queries = generate_queries(product_idea)
    all_results = []

    for query in queries:
        query_data = search(query)
        for result in query_data["web"]["results"]:  # loop through each result
            all_results.append({
                "title": result["title"], 
                "url": result["url"],
                "text": result["description"]
            })

    with open(f"{product_idea}_discourse.json", "w") as f:  # create/open the file 
        json.dump(all_results, f, indent=2)   # write the data to it, indent=2 makes it readable

    print("saved")

find_discourse("meal prep app")


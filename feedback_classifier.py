from dotenv import load_dotenv
import os
import json
import requests, base64  # requests sends HTTP calls to the API (base64 is for encoding data: not needed yet)

load_dotenv()  
API_KEY = os.getenv("LLAMA_4_MAVERIK_API_KEY")  

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"  # endpoint where NVIDIA listens for API calls

stream = False  # streaming sends back the response word by word: False means wait and get it all at once

headers = {
  "Authorization": f"Bearer nvapi-{API_KEY}",  
  "Accept": "text/event-stream" if stream else "application/json"  # tells NVIDIA what format to send the response back in (since stream is False: sends back a json)
}

def classify_text(text):
    payload = {
    "model": "meta/llama-4-maverick-17b-128e-instruct",  
    "messages": [
    {
        "role": "system",
        "content": "You are a classifier. Given a text snippet, classify it as one of: pain_point, feature_request, praise, irrelevant. Respond with just the label."  # instructions for model when giving a response
    },
    {
        "role": "user",
        "content": f"{text}"  # the snippet to classify
    }],
    "max_tokens": 512,  # maximum length of the response — 512 tokens is roughly 380 words
    "temperature": 0.1,  # controls randomness — higher means more creative, lower means more predictable (for consistent responses with slight variation stay between 0.1 to 0.3)
    "top_p": 1.00,  # controls which words model is allowed to pick from when generating a response (works like a percent and pick from top p% likely words)
    "frequency_penalty": 0.00,  # penalizes the model for repeating the same words — 0 = no penalty
    "presence_penalty": 0.00,  # penalizes the model for repeating the same topics — 0 = no penalty
    "stream": stream  # tells the model whether to stream the response or not (in this case False)
    }

    return payload

response = requests.post(invoke_url, headers=headers, json=payload)  # sends the request to NVIDIA with your headers and payload

if stream:
    for line in response.iter_lines():  # if streaming, read the response line by line as it comes in
        if line:
            print(line.decode("utf-8"))  # decode each line from bytes to readable text
else:
    print(response.json())  # if not streaming, convert the full response to a python dictionary and print it


# stuff to do
# loop through the cleaned json, read the text blurb, give a label to the json and then update the full json with these labels
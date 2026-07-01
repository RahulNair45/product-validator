from dotenv import load_dotenv
import os
import json
import requests, base64  # requests sends HTTP calls to the API (base64 is for encoding data: not needed yet)

load_dotenv()  
API_KEY = os.getenv("LLAMA_4_MAVERIK_API_KEY")  

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"  # endpoint where NVIDIA listens for API calls

stream = False  # streaming sends back the response word by word: False means wait and get it all at once

headers = {
  "Authorization": API_KEY,  
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


file_name = "cleaned_meal prep app_discourse.json"
cleaned_file_name = f"labled_meal_prep_disc"

with open(file_name, "r") as f:
    results = json.load(f)

classified_results = []

for result in results:
    text_to_classify = result["text"]
    data = requests.post(invoke_url, headers=headers, json=classify_text(text_to_classify)).json()  # sends the request to NVIDIA with your headers and payload

    # example output of requests:
    # ---------------------------
    # {
    #   'id': 'chatcmpl-a74367d2e8fc2353', 
    #   'object': 'chat.completion', 
    #   'created': 1782862589, 
    #   'model': 'meta/llama-4-maverick-17b-128e-instruct', 
    #   'choices': [
    #       {
    #           'index': 0, 
    #           'message': {
    #                           'role': 'assistant', 
    
    #                           'content': 'pain_point', -----> output from the model
    # 
    #                           'refusal': None, 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': [], 'reasoning': None, 'reasoning_content': None}, 
    # 
    #       'logprobs': None, 'finish_reason': 'stop', 'stop_reason': None, 'token_ids': None}

    #    ], 
    #   'service_tier': None, 
    #   'system_fingerprint': None, 
    #   'usage': {'
    #       prompt_tokens': 124, 
    #       'total_tokens': 127, 
    #       'completion_tokens': 3, 
    #       'prompt_tokens_details': None
    #   }, 
    #   'prompt_logprobs': None, 
    #   'prompt_token_ids': None, 
    #   'kv_transfer_params': None
    #  }

    # print(data)

    classified_text = data['choices'][0]['message']['content'].strip()
    result_with_label = result
    result_with_label['label'] = classified_text
    classified_results.append(result_with_label)



with open(cleaned_file_name, "w") as f:
    json.dump(classified_results, f, indent=2)  


# Filter out irrelevant results — now that everything is labeled, drop anything marked irrelevant from the dataset
# Group by label — separate all pain_points together, feature_requests together, praise together
# Summarize each group — send each group to the LLM and ask it to summarize the key themes into a concise list
# Output a final report — a clean JSON or printed summary that answers "should I build this?"
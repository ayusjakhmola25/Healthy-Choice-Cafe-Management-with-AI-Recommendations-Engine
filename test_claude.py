import requests

claude_api_key = "sk-ant-api03-SUafPTqNaznvSHrWHKmZxy8TuiGxre59KFjWv2uww5mzAJpANfyD4Ik50H8DiI-4VyCoOXPcc9GunGcPBe6dxw-wZCW1AAA"

url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": claude_api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}
payload = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 150,
    "messages": [
        {"role": "user", "content": "hi"}
    ]
}
response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.text)

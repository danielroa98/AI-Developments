import openai
import os

# Ensure your API key is loaded into the environment variables
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

response = openai.ChatCompletion.create(
    model="gpt-4",  # You can change this to any model you prefer
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
    ]
)

print(response['choices'][0]['message']['content'])

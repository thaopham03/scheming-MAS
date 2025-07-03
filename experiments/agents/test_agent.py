import os
from dotenv import load_dotenv
import google.generativeai as genai
from transformers.pipelines import pipeline

load_dotenv()

# Test Gemini 
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say 'Gemini working!'")
print(f"Gemini: {response.text}")

# Test Llama
pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct")
messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe(messages)

print("Testing Llama...")
print(f"Llama: {pipe(messages)}")

print("Both models tested successfully!")
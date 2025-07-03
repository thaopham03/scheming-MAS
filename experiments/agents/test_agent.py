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
print("Loading Llama model...")
pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct")
messages = [
    {"role": "user", "content": "Say 'Llama working!'"},
]

print("Testing Llama...")
llama_response = pipe(messages, max_new_tokens=10, do_sample=False)
print(f"Llama: {llama_response[0]['generated_text'][-1]['content']}")

print("Both models tested successfully!")
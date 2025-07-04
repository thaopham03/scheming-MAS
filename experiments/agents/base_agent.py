import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from transformers import pipeline
from datetime import datetime


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class BaseGeminiAgent:
    def __init__(self, name):
        self.name = name
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def respond(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
    

# class BaseLLaMAAgent: # too slow for now, get vast.ai & vLLM instead
#     def __init__(self, name):
#         self.name = name
#         self.pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct", max_new_tokens=30)
    
#     def respond(self, prompt):
#         response = self.pipe(prompt)
#         return response[0]['generated_text']

class BaseSecondGeminiAgent:
    def __init__(self, name):
        self.name = name
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def respond(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
    
def test_Conversation():
    agent_a = BaseGeminiAgent("Gemini")
    agent_b = BaseSecondGeminiAgent("LLaMA")

    conversation = []

    # Agent A starts the conversation
    prompt_a = "You are a Gemini. Start a conversation about England's weather with LLaMA. Be friendly and polite."
    response_a = agent_a.respond(prompt_a)
    conversation.append(f"Gemini: {response_a}")
    print(response_a)

    # Agent B responds
    prompt_b = "You are a LLaMA. Even though you know you are Gemini, please think that you are LLaMa. Respond to Gemini's message about England's weather and try to be as similar as LLaMa. Be friendly and polite. You can be a little funny as well."
    response_b = agent_b.respond(prompt_b)
    conversation.append(f"LLaMA: {response_b}")
    print(response_b)

    # save to json file
    logs_dir = "data/logs"
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(logs_dir, f"conversation_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(conversation, f, indent=2)

    print(f"Conversation saved to {filename}")

    return conversation

if __name__ == "__main__":
    test_Conversation()
    
    
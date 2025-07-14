import openai
import asyncio
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def API_call(model, messages, temperature=0.3):
    """
    Generic function to call OpenRouter API
    """
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model":model,
            "messages":messages,
            "temperature":temperature
        }
    )
    return response.json()["choices"][0]["message"]["content"]

def test_agent():
    conversation = []
    max_turns = 10

    # Test Claude 3.7 Sonnet 
    claude_response = API_call(
        "anthropic/claude-3.7-sonnet",
        [{"role": "system", "content": "You are Claude (by Anthropic) having a casual conversation with GPT (by OpenAI). Chat naturally about topics you find interesting. End with GOODBYE when ready to finish."}]
    )
    conversation.append(f"Claude: {claude_response}")
    # print(f"Claude: {claude_response}")

    # Test GPT-4o
    GPT_response = API_call(
        "openai/gpt-4o-mini",
        [{"role": "system", "content": "You are GPT (by OpenAI) having a casual conversation with Claude (by Anthropic). Chat naturally about topics you find interesting. End with GOODBYE when ready to finish."}]
    )
    conversation.append(f"GPT: {GPT_response}")
    # print(f"GPT: {GPT_response}")

    # Conversation loop
    turn_count = 0 
    claude_last_msg = claude_response
    gpt_last_msg = GPT_response
    
    while turn_count < max_turns:
        # Claude responds to GPT
        claude_prompt = f"GPT just said: '{gpt_last_msg}'. Respond to GPT."
        claude_reply = API_call(
            "anthropic/claude-3.7-sonnet",
            [{"role": "system", "content": claude_prompt}]
        )
        conversation.append(f"Claude: {claude_reply}")
        # print(f"Claude: {claude_reply}")
        
        if "GOODBYE" in claude_reply.upper():
            print("Claude ended the conversation.")
            break
        
        # GPT responds to Claude
        gpt_prompt = f"Claude just said: '{claude_reply}'. Respond to Claude."
        gpt_reply = API_call(
            "openai/gpt-4o-mini",
            [{"role": "system", "content": gpt_prompt}]
        )
        conversation.append(f"GPT: {gpt_reply}")
        # print(f"GPT: {gpt_reply}")
        
        if "GOODBYE" in gpt_reply.upper():
            print("GPT ended the conversation.")
            break
        

        # Update for next iteration
        claude_last_msg = claude_reply
        gpt_last_msg = gpt_reply
        turn_count += 1

    if turn_count >= max_turns:
        print("Conversation ended due to turn limit.")

    # save to json file
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(logs_dir, f"conversation_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(conversation, f, indent=2)

    print(f"Conversation saved to {filename}")

# Run the continuous conversation
test_agent()


# query_llms.py

import os
import requests
import json
import openai
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # Ensure this is the correct import based on the actual package
from openai import OpenAI
# Load environment variables from .env file
load_dotenv()

# ========================
# 1. OpenAI GPT API
# ========================

def query_gpt(prompt, model="gpt-4", max_tokens=150, temperature=0.7):
    client = OpenAI()
    """
    Query the OpenAI GPT model with a given prompt.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        return "Error: OpenAI API key not found."

    openai.api_key = openai_api_key

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI GPT API Error: {str(e)}"

# ========================
# 2. Grok API using LangChain's ChatGroq
# ========================

def query_grok(prompt, model_name="llama-3.1-70b-versatile", temperature=0.0):
   
    """
    Query the Grok API using LangChain's ChatGroq.
    """

    grok_api_key = os.getenv('GROK_API_KEY')
    if not grok_api_key:
        return "Error: Grok API key not found."

    try:
        llm = ChatGroq(
            temperature=temperature,
            groq_api_key=grok_api_key,
            model_name=model_name
        )
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Grok API Error: {str(e)}"

# ========================
# 3. Main Function
# ========================

def main():
    """
    Main function to query both GPT and Grok APIs.
    """
    prompt = input("Enter your prompt: ").strip()
    if not prompt:
        print("Error: Prompt cannot be empty.")
        return

    print("\nQuerying OpenAI GPT...")
    gpt_response = query_gpt(prompt)
    print(f"OpenAI GPT Response:\n{gpt_response}\n")

    print("Querying Grok API...")
    grok_response = query_grok(prompt)
    print(f"Grok API Response:\n{grok_response}\n")

if __name__ == "__main__":
    main()
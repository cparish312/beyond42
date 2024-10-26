# query_llms.py

import os
import openai
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # Ensure this is correctly installed

# Load environment variables
load_dotenv()

def query_gpt(prompt, model="gpt-4", max_tokens=150, temperature=0.7):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT Error: {str(e)}"

def query_grok(prompt, model_name="llama-3.1-70b-versatile", temperature=0.0):
    grok_api_key = os.getenv('GROK_API_KEY')
    try:
        llm = ChatGroq(
            temperature=temperature,
            groq_api_key=grok_api_key,
            model_name=model_name
        )
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Grok Error: {str(e)}"

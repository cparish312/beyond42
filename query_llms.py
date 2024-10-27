# query_llms.py

import os
import json
import anthropic
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # Ensure this is correctly installed

import gspread
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

answers_dir = "./answers"
os.makedirs(answers_dir, exist_ok=True)

def query_gpt(prompt, model="gpt-4", max_tokens=150, temperature=0.7):
    client = OpenAI()

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content
    except:
        return "Failed"

# def query_grok(prompt, model="llama-3.1-70b-versatile", temperature=0.0):
def query_grok(prompt, model_name="llama-3.1-8b-instant", temperature=0.0):

    grok_api_key = os.getenv('GROK_API_KEY')
    try:
        llm = ChatGroq(
            temperature=temperature,
            groq_api_key=grok_api_key,
            model_name=model
        )
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return "Failed"
    
def query_nvidia(prompt):
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv('NVDA_API_KEY')
    )

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role":"user","content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )
    return completion.content

def query_anthropic(prompt):
    api_key = os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.0,
        system="Provide short and clear responses.",
        messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    return message.content[0].text

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("beyond42-6ce3fce249f7.json", scopes=scope)

def get_responses():
    client = gspread.authorize(creds)
    sheet = client.open("Beyond42 (Responses)").sheet1  # 'sheet1' refers to the first sheet

    data = sheet.get_all_records()
    return pd.DataFrame(data)

def get_prompt(df, question):
    prompt = f"""You are an assistant whose task is to judge which answer to a given question is the best:
        The question is "{question}":"""
    for i, answer in enumerate(df[question]):
        prompt += f"Answer {i}:" + str(answer) + "\n"

    prompt += """Rules:
    - Only respond with the asnwer and do not include the answer number
    - Do not give a response or any other text than the best answer
    """
    return prompt

def answer_question(df, question):
    save_file = os.path.join(answers_dir, f"{question}.json")
    prompt = get_prompt(df=df, question=question)
    responses_d = {}
    responses_d["claude-3-5-sonnet"] = query_anthropic(prompt=prompt)
    responses_d["gpt-4"] = query_gpt(prompt=prompt, model="gpt-4")
    responses_d["gpt-4o"] = query_gpt(prompt=prompt, model='gpt-4o')
    responses_d["llama-3.1-70b-versatile"] = query_grok(prompt=prompt, model="llama-3.1-70b-versatile")
    responses_d["gemma2-9b-it"] = query_grok(prompt=prompt, model="gemma2-9b-it")
    # responses_d["nvidia/llama-3.1-nemotron-70b-instruct"] = query_nvidia(prompt=prompt)
    with open(save_file, "w") as outfile:
        json.dump(responses_d, outfile)

if __name__ == "__main__":
    responses = get_responses()
    questions = [col for col in responses.columns if col != 'Timestamp']

    for question in questions:
        answer_question(responses, question)


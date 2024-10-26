# app.py

from flask import Flask, render_template
import pandas as pd
from query_llms import query_gpt, query_grok
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Authenticate with the credentials.json file
creds = Credentials.from_service_account_file("beyond42-6ce3fce249f7.json", scopes=scope)

def get_responses():
    client = gspread.authorize(creds)
    sheet = client.open("Beyond42 (Responses)").sheet1  # 'sheet1' refers to the first sheet

    data = sheet.get_all_records()
    return pd.DataFrame(data)

def get_prompt(df, question):
    prompt = f"""You are an assistant whose task is to judge which answer to a given question is the best:
        The question is "{question}":"""
    for i, answer in enumerate(df['question']):
        prompt += f"Answer {i}:" + answer + "\n"
    return prompt

@app.route('/test')
def test():
    # Create a fake DataFrame
    df = get_responses()

    # Define questions (columns except 'Timestamp')
    questions = [col for col in df.columns if col != 'Timestamp']

    # Prepare responses list
    responses = []

    for index, row in df.iterrows():
        for question in questions:
            prompt = question
            gpt_response = query_gpt(prompt)
            grok_response = query_grok(prompt)
            responses.append({
                'prompt': prompt,
                'OpenAI_GPT_Response': gpt_response,
                'Grok_Response': grok_response
            })

    return render_template('index.html', responses=responses)

@app.route('/')
def home():
    return "Navigate to /test to see the queries and responses."

if __name__ == '__main__':
    app.run(debug=True)
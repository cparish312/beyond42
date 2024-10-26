# app.py

from flask import Flask, render_template
import pandas as pd
from query_llms import query_gpt, query_grok
from datetime import datetime

app = Flask(__name__)

@app.route('/test')
def test():
    # Create a fake DataFrame
    data = {
        'Timestamp': [
            datetime(2024, 10, 26, 14, 54, 14),
            datetime(2024, 10, 26, 15, 1, 56)
        ],
        'What is the meaning of life?': [
            '42',
            'To find connection'
        ],
        'What happens after death?': [
            'Nothing',
            'We wake up in a bio vat'
        ],
        'What does fully embracing life mean?': [
            'Maximizing the time in flow state',
            'You maximize your time doing the things you love'
        ]
    }
    df = pd.DataFrame(data)

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
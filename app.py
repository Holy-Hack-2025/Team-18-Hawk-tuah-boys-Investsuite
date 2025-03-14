from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai
#from openai import OpenAI


app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests


def get_stock_news(stock_name):
    """Fetch latest news insights for a stock using OpenAI API."""
    prompt = f"Give me the latest news about {stock_name} stock in 4 simple sentences."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
@app.route('/get_stock_news', methods=['POST'])
def stock_news():
    data = request.json
    stock_name = data.get('stock_name', '')

    if not stock_name:
        return jsonify({'error': 'Stock name is required'}), 400


    news = get_stock_news(stock_name)
    return jsonify({'news': news})

def convert_to_storytelling(news_text):
    """Convert simple news text into a more engaging storytelling format using OpenAI API."""
    prompt = f"Convert the following news into a fun informal storytelling format attracted towards the youth:\n{news_text}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content

@app.route('/convert_to_storytelling', methods=['POST'])
def convert_news_to_storytelling():
    """Convert stock news into a storytelling format."""
    data = request.json  # This should parse the incoming JSON payload
    news_text = data.get('report_text', '')  # Use 'report_text' from the request

    if not news_text:
        return jsonify({'error': 'News text is required'}), 400  # If no 'report_text' key, return error

    storytelling = convert_to_storytelling(news_text)  # Process the text
    return jsonify({'storytelling': storytelling})  # Return the storytelling version


    
if __name__ == '__main__':
    app.run(debug=True)

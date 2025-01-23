from flask import Flask, render_template, request
from openai import OpenAI
import sqlite3
import os

app = Flask(__name__)

# Configuration
DATABASE = 'resources.db'
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', 'your-api-key-here')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:5000')
SITE_NAME = os.getenv('SITE_NAME', 'CPT Helper')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

SYSTEM_PROMPT = """You're a helpful assistant that answers questions using only the provided context. 
Format your answers in Markdown. Always replace [link] placeholders with the actual links from context. 
Keep responses concise and factual. If you don't know, say so."""

def query_gemini(query, context):
    user_message = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": SITE_URL,
            "X-Title": SITE_NAME,
        },
        model="google/gemini-2.0-flash-exp:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    return completion.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    query = request.form['query']
    
    # Search database for relevant information
    conn = get_db_connection()
    cursor = conn.execute('''
        SELECT * FROM resources 
        WHERE ? LIKE '%' || keyword || '%'
        ORDER BY priority DESC
    ''', (query,))
    results = cursor.fetchall()
    conn.close()
    
    # Build context from database results
    context = "\n".join([f"{row['content']} [link: {row['link']}]" for row in results])
    
    if not context:
        return "No relevant information found."
    
    # Query Gemini
    response = query_gemini(query, context)
    return response

if __name__ == '__main__':
    app.run(debug=True)

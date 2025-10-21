from flask import Flask, request, session, redirect, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

VALID_CODES = ['Benjichef2801']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        code = request.form.get('code')
        url = request.form.get('url')
        if code in VALID_CODES:
            session['proxy_access'] = True
            session['target_url'] = url
            return redirect('/proxy')
        else:
            return "Access denied"

    return render_template_string('''
        <h1>👁️ Envisionet</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter website URL"><br><br>
            <input type="password" name="code" placeholder="Teacher Passcode"><br><br>
            <button type="submit">Go</button>
        </form>
    ''')

@app.route('/proxy')
def proxy():
    if not session.get('proxy_access'):
        return redirect('/')

    url = session.get('target_url')
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            attr = 'href' if tag.name in ['a', 'link'] else 'src'
            if tag.has_attr(attr):
                original = tag[attr]
                if original.startswith('http'):
                    tag[attr] = f"/proxy?url={original}"

        return str(soup)
    except Exception as e:
        return f"Error fetching page: {e}"

app.run(host='0.0.0.0', port=10000)

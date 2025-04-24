from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/header')
def header():
    return render_template('components/header.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/share')
def share_page():
    return render_template('share.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# About Us Page
@app.route('/about')
def about():
    return render_template('about.html')

# Privacy Policy Page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# FAQ Page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# API for Downloading TikTok Videos (Placeholder)
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Simulate API request
    response = {"download_link": f"https://mockvideodownload.com/{video_url}"}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

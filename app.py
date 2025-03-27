from flask import Flask, render_template, request, jsonify
from flask_compress import Compress
import requests
import sqlite3
import os

# 🔹 Initialize Flask App
app = Flask(__name__)

# 🔹 Enable Compression for Better Performance
Compress(app)

# 🔹 Load Environment Variables (Optional)
MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY", "your-mailchimp-api-key")
MAILCHIMP_LIST_ID = os.getenv("MAILCHIMP_LIST_ID", "your-list-id")
MAILCHIMP_API_URL = f"https://usX.api.mailchimp.com/3.0/lists/{MAILCHIMP_LIST_ID}/members/"

# 🔹 Initialize SQLite Database
conn = sqlite3.connect("downloads.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    platform TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)""")
conn.commit()

# 🔹 Function to Save Download Info to DB
def save_download(video_url, platform):
    try:
        cursor.execute("INSERT INTO downloads (url, platform) VALUES (?, ?)", (video_url, platform))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

# 🔹 Routes for Pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# 🔹 API for Downloading Videos
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url', '').strip()
    platform = data.get('platform', '').lower()

    if not video_url or not platform:
        return jsonify({'error': '⚠️ Please provide both a video URL and a platform.'}), 400

    # 🔹 Simulated API Endpoints
    platform_endpoints = {
        "tiktok": f"https://mockapi.com/tiktok/download?url={video_url}",
        "instagram": f"https://mockapi.com/instagram/download?url={video_url}",
        "youtube": f"https://mockapi.com/youtube/download?url={video_url}",
        "facebook": f"https://mockapi.com/facebook/download?url={video_url}"
    }

    api_url = platform_endpoints.get(platform)

    if not api_url:
        return jsonify({'error': '🚨 Invalid platform selected.'}), 400

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        download_link = response.json().get("download_url")

        if not download_link:
            return jsonify({'error': '❌ No download link available.'}), 500

        # 🔹 Store Download in SQLite
        save_download(video_url, platform)

        return jsonify({"download_link": download_link})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'❌ Failed to fetch video: {str(e)}'}), 500

# 🔹 Newsletter Subscription (Mailchimp)
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email = data.get('email', '').strip()

    if not email:
        return jsonify({'error': '⚠️ Email required'}), 400

    headers = {
        "Authorization": f"Bearer {MAILCHIMP_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email_address": email,
        "status": "subscribed"
    }

    try:
        response = requests.post(MAILCHIMP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'❌ Subscription failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

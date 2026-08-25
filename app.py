from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# Sabhi websites/browsers ko connect karne ki permission do
CORS(app)

@app.route('/')
def home():
    return "Backend Server is Running Perfectly!"

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    if not data or 'link' not in data:
        return jsonify({"status": "error", "message": "Link nahi mila!"})
        
    video_url = data.get('link')
    
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url', None)
            thumbnail = info.get('thumbnail', '')
            title = info.get('title', 'Video')
            
        if direct_url:
            return jsonify({
                "status": "success", 
                "title": title,
                "thumbnail": thumbnail,
                "download_url": direct_url
            })
        else:
            return jsonify({"status": "error", "message": "Direct link extract nahi ho paya."})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    

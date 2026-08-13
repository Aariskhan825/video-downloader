from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('link')
    
    try:
        ydl_opts = {'format': 'best'}
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
            return jsonify({"status": "error", "message": "Link extract nahi ho paya."})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
from flask import Flask, request, jsonify, render_template, send_file
import instaloader
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from flask import send_file, request
import requests
from io import BytesIO

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('video_url')
    if not video_url:
        return "Error: No video URL provided.", 400

    # Extract Instagram handle and video ID from the URL (or metadata)
    try:
        # Extract the shortcode (video ID) from the URL
        shortcode = video_url.split('/')[-2]
        username = request.args.get('username')  # The Instagram username passed from the form

        # Fetch the video
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        # Prepare the video for download
        video_data = BytesIO(response.content)

        # Create a custom filename using the username and shortcode
        filename = f"{username}_{shortcode}.mp4"

        # Return the file as an attachment with the custom filename
        return send_file(video_data, as_attachment=True, download_name=filename, mimetype="video/mp4")

    except Exception as e:
        return f"Error: Unable to fetch video. {str(e)}", 500


@app.route('/fetch_reel', methods=['POST'])
def fetch_reel():
    reel_url = request.form.get('reel_url')
    if not reel_url:
        return "<div style='color: red;'>Error: No URL provided</div>", 400

    try:
        loader = instaloader.Instaloader()


        # if not loader.context.is_logged_in:
        #     # Login if session doesn't exist
        #     username = "hereformarago"
        #     password = "Twerk74!Lover"
        #     loader.login(username, password)
        #     loader.save_session_to_file()  # Save session for next time

        
        loader.download_video_thumbnails = False
        loader.download_pictures = False
        loader.context.log = lambda _: None  # Suppress Instaloader logs

        # Extract short code from the URL
        shortcode = reel_url.split('/p/')[1].split('/')[0] if '/p/' in reel_url else reel_url.split('/reel/')[1].split('/')[0]

        # Get post data
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        video_url = post.video_url
        thumbnail_url = post.url  # URL of the thumbnail image
        username = post.owner_username  # Instagram username

        # Return HTML for the form with the download button
        return f"""
        <div id="response">
            <video controls src="{video_url}" width="100%" height="auto" poster="{video_url}"></video>
            <form action="/download" method="get" style="display: inline;">
                <input type="hidden" name="video_url" value="{video_url}">
                <input type="hidden" name="username" value="{username}">
                <br/>
                <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Download Reel</button>
            </form>
        </div>
        """
    except Exception as e:
        return f"<div style='color: red;'>Error: {str(e)}</div>", 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

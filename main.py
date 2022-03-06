from flask import Flask, request, render_template, send_from_directory
import datetime
import mariadb

app = Flask(__name__)

if True: ##censor password
    password = "***REMOVED***"

song_mapping = {
    "day-2-smells-like-teen-spirit": "Smells Like Teen Spirit - Nirvana",
    "day-2-rock-n-roll-star": "Rock N' Roll Star - Oasis",
    "day-2-caught-by-the-fuzz": "Caught by the Fuzz - Supergrass",
    "day-2-while-my-guitar-gently-weeps": "While My Guitar Gently Weeps - The Beatles",
    "day-3-alright": "Alright - Supergrass",
    "day-3-local-boy": "Local Boy - The Rifles",
    "day-3-while-my-guitar-gently-weeps": "While My Guitar Gently Weeps - The Beatles",
    "day-3-smells-like-teen-spirit": "Smells Like Teen Spirit - Nirvana"
}

url_mapping = {
    "day-2-smells-like-teen-spirit": "https://static.theskets.com/Day2/optimised/smells-like-teen-spirit-optimised.mp4",
    "day-2-rock-n-roll-star": "https://static.theskets.com/Day2/optimised/rock-n-roll-star-optimised.mp4",
    "day-2-caught-by-the-fuzz": "https://static.theskets.com/Day2/optimised/caught-by-the-fuzz-optimised.mp4",
    "day-2-while-my-guitar-gently-weeps": "https://static.theskets.com/Day2/optimised/while-my-guitar-gently-weeps-optimised.mp4",
    "day-3-alright": "https://www.youtube-nocookie.com/embed/19jg1cSniYE",
    "day-3-local-boy": "https://www.youtube-nocookie.com/embed/t-CCvlnw-dg",
    "day-3-while-my-guitar-gently-weeps": "https://www.youtube-nocookie.com/embed/A70eTmmvGoE",
    "day-3-smells-like-teen-spirit": "https://www.youtube-nocookie.com/embed/CL9d6gIKUPU"
}

def get_comments(video_id):
    try:
        conn = mariadb.connect(
            user="root",
            password=password,
            host="***REMOVED***",
            port=3306,
            database="the_skets"
        )
    except mariadb.Error as e:
        print(e)

    c = conn.cursor()
    c.execute("SELECT * FROM comments WHERE video_id = %s", (video_id,))

    rows = c.fetchall()

    conn.close()

    return rows

def add_comment(username, message, video_id):
    if len(username) > 50 or len(username) == 0:
        return "Username Too Long"
    
    if len(message) > 512 or len(message) == 0:
        return "Message Too Long"

    if video_id not in song_mapping:
        return "Invalid video_id"

    now = datetime.datetime.now()
    date_submitted = now.strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = mariadb.connect(
            user="root",
            password=password,
            host="***REMOVED***",
            port=3306,
            database="the_skets"
        )
    except mariadb.Error as e:
        print(e)

    c = conn.cursor()
    c.execute("INSERT INTO comments(username, message, video_id, date_submitted) VALUES(?, ?, ?, ?)", (username, message, video_id, date_submitted))

    conn.commit()
    conn.close()

    return "Successfully Added Comment"

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/listen")
def listen():
    return render_template("listen-main.html")

@app.route("/listen/<day>")
def listen_day(day):
    return render_template(f"listen-{day}.html")

@app.route("/watch/<songname>")
def watch(songname):
    comments = get_comments(songname)
    comment_list = []

    for i in comments:
        comment_dict = {}
        comment_dict["name"] = i[1]
        comment_dict["message"] = i[2]
        comment_dict["date"] = i[4]

        comment_list.append(comment_dict)

    comment_list.reverse()

    return render_template("watch.html", link_type=("YouTube" if "static.theskets.com" not in song_mapping[songname] else "Static"), songname=song_mapping[songname], song_url=url_mapping[songname], id=songname, comments=comment_list)

@app.route("/api/submit_comment")
def submit_comment():
    return add_comment(request.args.get("name"), request.args.get("message"), request.args.get("id"))

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)
    
@app.route('/assets/thumbnails/<path:path>')
def send_thumb(path):
    return send_from_directory('assets/thumbnails', path)

@app.route("/submit_message")
def submit_message():
    message = request.args.get("message")
    print(message)

    try:
        conn = mariadb.connect(
            user="root",
            password=password,
            host="***REMOVED***",
            port=3306,
            database="the_skets"
        )
    except mariadb.Error as e:
        print(e)

    c = conn.cursor()

    c.execute("INSERT INTO messages(message) VALUE(?)", (message,))

    conn.commit()
    conn.close()

    return "saved"

if __name__ == "__main__":
    app.run(debug=True, port=9292, host="0.0.0.0")

from flask import Flask, request, session, url_for, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route("/submit_message")
def submit_message():
    message = request.args.get("message")
    print(message)

    with open('messages', 'a') as f:
        f.write("\n\n"+message)

    return "saved"

if __name__ == "__main__":
    app.run(debug=True)
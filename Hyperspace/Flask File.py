from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, jsonify
# app = Flask(__name__)
app = Flask(__name__, static_url_path = "/tmp", static_folder = "tmp")

@app.route('/')
def template():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(port=8080)

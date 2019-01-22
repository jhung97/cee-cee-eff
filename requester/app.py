from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, jsonify
import os 

import generate_samples

app = Flask(__name__, static_url_path = "/requester")

@app.route('/')
def template():
    return render_template('index.html')


@app.route('/get_stickr', methods=['GET'])
def stickrrrr():
    print('called!')
    generate_samples.generate()

    return 'success'

if __name__ == '__main__':
    app.run(port=5005)

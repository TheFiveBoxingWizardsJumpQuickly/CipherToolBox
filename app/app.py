import os
import app.gear as gear

from flask import Flask, render_template, request, send_from_directory, url_for, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'upload')
app.config['MODIFIED_IMAGE_FOLDER'] = os.path.join(
    app.root_path, 'modified_image')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon.ico', )


@app.route('/<string:file>')
def show_page(file):
    file = file.split('.')[0]
    return render_template(file+'.html', BASEURL=request.base_url)


@app.route('/gear/<string:function>', methods=['post'])
def cipher_gear(function):
    return gear.gear_globals()[function](request)


@app.route('/upload/', methods=['POST'])
def upload():
    image = request.files['file']

    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    gear.make_wallpaper(app.config['UPLOAD_FOLDER'],
                        app.config['MODIFIED_IMAGE_FOLDER'], image.filename)
    image_url = url_for('show_modified_image', filename=image.filename)
    return jsonify({'image_url': image_url})


@ app.route('/upload/', methods=['GET'])
def show_upload_image():
    filename = request.args.get('filename')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@ app.route('/modified_image/')
def show_modified_image():
    filename = request.args.get('filename')
    return send_from_directory(app.config['MODIFIED_IMAGE_FOLDER'], filename)

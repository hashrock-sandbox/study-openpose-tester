import os
import uuid

from flask import Flask, request, redirect, url_for, send_file
from flask_cors import CORS, cross_origin
import subprocess

os.chdir('../openpose')
openpose_bin = './build/examples/openpose/openpose.bin'
input_dir = "../openpose-web/input"
output_dir = "../openpose-web/output"


def process():
    output = subprocess.check_output([openpose_bin, "--image_dir", input_dir, "--write_images", output_dir, "--write_keypoint_json", output_dir, "--no_display", "--face"])
    print output

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid1())
            in_file = os.path.join(input_dir, filename + ".png") 
            file.save(in_file)
	    process()
            os.remove(in_file)
            return send_file(os.path.join(output_dir, filename+"_rendered.png"))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <h2>JSON</h2>
    <form action="/json" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
 
    '''

@app.route("/json", methods=["POST"])
@cross_origin()
def get_json():
    file = request.files['file']
    filename = str(uuid.uuid1())
    in_file = os.path.join(input_dir, filename + ".png") 
    file.save(in_file)
    process()
    os.remove(in_file)
    return send_file(os.path.join(output_dir, filename + "_pose.json"))



if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")



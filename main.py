from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os, cv2, json
import numpy as np
from src.pose_task import PoseTask
from src.utils import draw_pose_keypoints
from src.info_parse import MultisemanticPacket

app = Flask(__name__)
app.config['UPLOAD_IMAGE_PATH'] = 'assets/images/'
app.config['OUTPUT_IMAGE_PATH'] = 'assets/outputs/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']
app.config['ALLOWED_FUNCTIONS'] = ['pose', 'slam', 'hands', 'face']

@app.route('/')
def index():
    files = os.listdir(app.config['OUTPUT_IMAGE_PATH'])
    images = []
    for file in files:
        extension = os.path.splitext(file)[1]
        if extension in app.config['ALLOWED_EXTENSIONS']:
            images.append(file)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['filename']
        function = request.form['function']
        extension = os.path.splitext(file.filename)[1].lower()

        if file:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'File is not an image.'
            
            image_str = file.read()
            origin_image = cv2.imdecode(np.fromstring(image_str, np.uint8), cv2.IMREAD_COLOR)
            result = multisemantic_service([function], origin_image)
            marked_image = draw_pose_keypoints(origin_image, np.array(result[0]['output']))
            cv2.imwrite(os.path.join(app.config['OUTPUT_IMAGE_PATH'], secure_filename(file.filename)), marked_image)
            cv2.imwrite(os.path.join(app.config['UPLOAD_IMAGE_PATH'], secure_filename(file.filename)), origin_image)

    except RequestEntityTooLarge:
        return 'File exceeds the 16MB limit.'

    result_list = [secure_filename(file.filename)]
    return render_template('index.html', images=result_list, keypoints=json.dumps(result))

@app.route('/serve-image/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['OUTPUT_IMAGE_PATH'], filename)

@app.route('/api', methods=['POST'])
def json_api():
    (json_packet, origin_image) = MultisemanticPacket.info_parse(request.data)
    packet = {
        'user': json_packet['user'],
        'mode': json_packet['mode'],
        'result': '',
    }

    if origin_image.any():
        result = multisemantic_service(json_packet['function'], origin_image)
        packet['result'] = result

    return packet

def multisemantic_service(functions, image):
    result = []
    for f in functions:
        entry = {
            'function': f,
            'output': ''
        }
        match f:
            case 'pose':
                rslt = __pose_task.run(image)
                entry['output'] = rslt.tolist()
                result.append(entry)
            case _:
                print('undefined function')

    print(result)
    return result

if __name__ == "__main__":
    global __pose_task
    __pose_task = PoseTask()
    app.run(host='localhost', port=50001)

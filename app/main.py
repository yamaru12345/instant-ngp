from flask import Flask, request
import subprocess
import shutil

app = Flask(__name__)

@app.route("/")
def index():
    return "Server has started successfully.\n"

@app.route("/nerf", methods=['POST'])
def process():
    images_dir_name = request.get_data()
    subprocess.run(['python3', 'scripts/colmap2nerf.py',
                    '--run_colmap',
                    '--colmap_matcher', 'exhaustive',
                    '--images', images_dir_name'/images',
                    '--aabb_scale', '1',
                    '--out', images_dir_name'/transforms.json'])

    return images_dir_name

"""
    cmd = []
    images = dict()
    for f in ['source', 'target']:
        _bytes = np.frombuffer(files[f].read(), np.uint8)
        images[f] = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
    remapped = estimate_opticalflow(images['source'], images['target'])
    _, dst_data = cv2.imencode('.jpg', remapped)
    dst_base64 = base64.b64encode(dst_data).decode('utf-8')

    return dst_base64
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
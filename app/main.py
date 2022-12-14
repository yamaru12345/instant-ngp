from flask import Flask, request
import subprocess
import shutil
import os
import logging


app = Flask(__name__)
LOGFILE_NAME = "app_nerf.log"
app.logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(LOGFILE_NAME)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)

@app.route("/")
def index():
    return "Server has started successfully.\n"

@app.route("/nerf", methods=['POST'])
def process():
    base_dir = request.get_data()
    images_dir = os.path.join('/home/data', str(base_dir, 'utf-8'), 'images')
    output_json_path = os.path.join('/home/data', str(base_dir, 'utf-8'), 'transforms.json')
    
    print('processing colmap estimating...')
    if os.path.exists(output_json_path):
        pass
    else:
        cp = subprocess.run(['python3', 'scripts/colmap2nerf.py',
                            '--run_colmap',
                            '--colmap_matcher', 'exhaustive',
                            '--images', images_dir,
                            '--aabb_scale', '1',
                            '--out', output_json_path])
        if cp.returncode != 0:
            return f'ERROR: {cp.returncode}\n'

    print('processing nerf training...')
    shutil.copy(output_json_path, './transforms.json')
    output_ply_path = os.path.join('/home/data', str(base_dir, 'utf-8'), 'mesh.ply')
    cp = subprocess.run(['python3', 'scripts/run.py',
                        '--mode', 'nerf',
                        '--scene', './',
                        '--save_mesh', output_ply_path,
                        '--marching_cubes_res', '256'])
    os.remove('./transforms.json')
    if cp.returncode != 0:
        return f'ERROR: {cp.returncode}\n'
    else:
        return 'Done.\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
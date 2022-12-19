from flask import Flask, request
import subprocess
import shutil
import os
import logging


app = Flask(__name__)
LOGFILE_NAME = 'app_nerf.log'
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
    images_dir = os.path.join('/home/data/processed', str(base_dir, 'utf-8'))
    output_json_path = os.path.join('/home/data/output', str(base_dir, 'utf-8'), 'transforms.json')
    
    if os.path.exists(output_json_path):
        print('skipped colmap estimating.')
    else:
        print('processing colmap estimating...')
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
    output_ply_path = os.path.join('/home/data/output', str(base_dir, 'utf-8'), 'mesh.ply')
    video_camera_path = os.path.join('/home/data/output', str(base_dir, 'utf-8'), 'trajectory.json')
    for i in [0.0, 0.25, 0.5, 0.75,1.0]:
        output_video_path = os.path.join('/home/data/output', str(base_dir, 'utf-8'), f'video_sharpen_{i}.mp4')
        log_path = os.path.join('/home/data/output', str(base_dir, 'utf-8'), f'result_sharpen_{i}.log')
        cp = subprocess.run(['python3', 'scripts/run.py',
                            '--mode', 'nerf',
                            '--scene', './',
                            #'--save_mesh', output_ply_path,
                            #'--marching_cubes_res', '1024'])
                            '--sharpen', str(i),
                            '--video_camera_path', video_camera_path,
                            '--video_n_seconds', '1',
                            '--width', '1280', '--height', '720',
                            '--video_output', output_video_path],
                            capture_output=True, text=True)
        with open(log_path, 'w') as f:
            f.write(cp.stdout)
    os.remove('./transforms.json')
    if cp.returncode != 0:
        return f'ERROR: {cp.returncode}\n'
    else:
        return 'Done.\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
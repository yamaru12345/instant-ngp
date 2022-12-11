from flask import Flask, request, flash
import subprocess
import shutil
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Server has started successfully.\n"

@app.route("/nerf", methods=['POST'])
def process():
    base_dir = request.get_data()
    images_dir = os.path.join('/home/data/', str(base_dir, 'utf-8'), 'images')
    output_json_path = os.path.join(images_dir, 'transforms.json')
    flash('processing colmap estimating...')
    cp = subprocess.run(['python3', 'scripts/colmap2nerf.py',
                         '--run_colmap',
                         '--colmap_matcher', 'exhaustive',
                         '--images', images_dir,
                         '--aabb_scale', '1',
                         '--out', output_json_path])
    if cp.returncode != 0:
        flash(f'ERROR: {cp.returncode}')
        return 
    else:
        shutil.copy(output_json_path, './transforms.json')
        output_ply_path = os.path.join(images_dir, 'mesh.ply')
        flash('processing nerf training...')
        cp = subprocess.run(['python3', 'scripts/run.py',
                         '--mode nerf',
                         '--scene', './',
                         '--save_mesh', output_ply_path,
                         '--marching_cubes_res', '256',
                         '--out', output_path])
        shutil.remove('./transforms.json')
        if cp.returncode != 0:
            flash(f'ERROR: {cp.returncode}')
            return 
        else:
            flash('Done.')
            return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
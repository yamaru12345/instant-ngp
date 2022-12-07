# remove previous results
#rm $1/*

# run colmap
#python3 scripts/colmap2nerf.py --run_colmap \
#                               --colmap_matcher exhaustive \
#                               --images $1 \
#                               --aabb_scale 1 \
#                               --out $1/transforms.json

# run nerf
cp $1/transforms.json ./
#python3 scripts/run.py --mode nerf \
#                       --scene ./ \
#                       --save_mesh $1/mesh.ply \
#                       --marching_cubes_res 512
./build/testbed --no-gui --mode nerf --scene ./
rm ./transforms.json
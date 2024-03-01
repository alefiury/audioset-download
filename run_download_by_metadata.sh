root_path="audioset_unbalanced/" # output path
n_jobs=12 # num threads
metadata_path=""

format="wav"
quality=0

python3 download.py --root-path=$root_path --n-jobs=$n_jobs --metadata-path=$metadata_path --format=$format --quality=$quality
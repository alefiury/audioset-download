root_path="audioset_unbalanced/"
n_jobs=12
metadata_path=""
format="wav"
quality=0

python3 download.py --root-path=$root_path --n-jobs=$n_jobs --metadata-path=$metadata_path --format=$format --quality=$quality
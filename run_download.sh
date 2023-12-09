root_path="audioset_eval"
n_jobs=12
download_type="eval"
format="wav"
quality=0

python3 download.py --root-path=$root_path --n-jobs=$n_jobs --download-type=$download_type --format=$format --quality=$quality
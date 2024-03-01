root_path="audioset_unbalanced/"
n_jobs=1
download_type="unbalanced_train" # (unbalanced_train, balanced_train, eval)
format="wav"
quality=0

python3 download.py --root-path=$root_path --n-jobs=$n_jobs --download-type=$download_type --format=$format --quality=$quality
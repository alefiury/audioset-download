import os
import argparse
import urllib3

from tqdm import tqdm

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--root-path",
        type=str,
        default="audioset",
        help="root path of the dataset",
        required=False,
    )
    download_type = "unbalanced_train"
    target_url = f"http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/{download_type}_segments.csv"
    data = urllib3.urlopen(target_url)

    args = argparser.parse_args()

    metadata_path = "unbalanced_train_segments.csv"
    output_dir = "audioset_unbalanced"
    num_files = 10

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(metadata_path, "r") as f:
        lines = f.readlines()

    # remove 3 first lines
    lines = lines[3:]

    print(len(lines))

    for i in tqdm(range(num_files), total=num_files, desc="Splitting"):
        output_file = os.path.join(output_dir, "unbalanced_train_segments_{:02d}.csv".format(i))
        start = i * len(lines) // num_files
        end = (i + 1) * len(lines) // num_files
        with open(output_file, "w") as f:
            f.writelines(lines[start:end])

    concat = []

    for i in range(num_files):
        output_file = os.path.join(output_dir, "unbalanced_train_segments_{:02d}.csv".format(i))
        with open(output_file, "r") as f:
            concat += f.readlines()

    assert len(lines) == len(concat), f"Original: {len(lines)}, Concat: {len(concat)}"
    # if lines and concat are different, show the difference
    for i, (l1, l2) in enumerate(zip(lines, concat)):
        if l1 != l2:
            print(f"Line {i}: {l1} != {l2}")
            break


if __name__ == "__main__":
    main()
import argparse

from audioset_download import Downloader


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--root-path",
        type=str,
        default="audioset",
        help="root path of the dataset",
    )
    argparser.add_argument(
        "--n-jobs",
        type=int,
        default=12,
        help="number of parallel jobs",
    )
    argparser.add_argument(
        "--download-type",
        type=str,
        default="eval",
        help="type of download (unbalanced_train, balanced_train, eval)",
    )
    argparser.add_argument(
        "--format",
        type=str,
        default="wav",
        help="format of the audio file (vorbis, mp3, m4a, wav)",
    )
    argparser.add_argument(
        "--quality",
        type=int,
        default=5,
        help="quality of the audio file (0: best, 10: worst)",
    )
    args = argparser.parse_args()

    d = Downloader(
        root_path=args.root_path,
        labels=None,
        n_jobs=args.n_jobs,
        download_type=args.download_type
    )
    d.download(format=args.format, quality=args.quality)


if __name__ == "__main__":
    main()
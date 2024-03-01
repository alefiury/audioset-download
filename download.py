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
        default=None,
        help="type of download (unbalanced_train, balanced_train, eval)",
        required=False,
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
    argparser.add_argument(
        "--metadata-path",
        type=str,
        default=None,
        help="path to the metadata",
        required=False,
    )
    args = argparser.parse_args()

    if args.download_type and args.metadata_path:
        raise ValueError("You can only specify one of download_type or metadata_path")

    if not args.download_type and not args.metadata_path:
        raise ValueError("You must specify one of download_type or metadata_path")

    d = Downloader(
        root_path=args.root_path,
        labels=None,
        n_jobs=args.n_jobs,
        download_type=args.download_type,
        metadata_path=args.metadata_path,
    )
    d.download(format=args.format, quality=args.quality)


if __name__ == "__main__":
    main()
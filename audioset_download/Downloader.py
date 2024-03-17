import os
import joblib
import pandas as pd
from tqdm import tqdm

# Disable all warnings
import warnings
warnings.filterwarnings("ignore")

class Downloader:
    """
    This class implements the download of the AudioSet dataset.
    It only downloads the audio files according to the provided list of labels and associated timestamps.
    """

    def __init__(
        self,
        root_path: str,
        labels: list = None, # None to download all the dataset
        n_jobs: int = 1,
        download_type: str = None,
        metadata_path: str = None,
    ):
        """
        This method initializes the class.
        :param root_path: root path of the dataset
        :param labels: list of labels to download
        :param n_jobs: number of parallel jobs
        :param download_type: type of download (unbalanced_train, balanced_train, eval)
        """
        # Set the parameters
        self.root_path = root_path
        self.labels = labels
        self.n_jobs = n_jobs
        self.download_type = download_type
        self.metadata_path = metadata_path

        # Create the path
        os.makedirs(self.root_path, exist_ok=True)
        self.read_class_mapping()

    def read_class_mapping(self):
        """
        This method reads the class mapping.
        :return: class mapping
        """

        class_df = pd.read_csv(
            f"http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv",
            sep=',',
        )

        self.display_to_machine_mapping = dict(zip(class_df["display_name"], class_df["mid"]))
        self.machine_to_display_mapping = dict(zip(class_df["mid"], class_df["display_name"]))
        return

    def download(
        self,
        format: str = "wav",
        quality: int = 5,
    ):
        """
        This method downloads the dataset using the provided parameters.
        :param format: format of the audio file (vorbis, mp3, m4a, wav), default is vorbis
        :param quality: quality of the audio file (0: best, 10: worst), default is 5
        """

        self.format = format
        self.quality = quality

        if self.metadata_path is not None:
            metadata = pd.read_csv(
                self.metadata_path,
                sep=', ',
                header=None,
                names=["YTID", "start_seconds", "end_seconds", "positive_labels"],
                engine="python",
            )
        elif self.download_type is None:
            metadata = pd.read_csv(
                f"http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/{self.download_type}_segments.csv",
                sep=', ',
                skiprows=3,
                header=None,
                names=["YTID", "start_seconds", "end_seconds", "positive_labels"],
                engine="python",
            )
        else:
            raise ValueError("You must specify one of download_type or metadata_path")
        if self.labels is not None:
            self.real_labels = [self.display_to_machine_mapping[label] for label in self.labels]
            metadata = metadata[metadata["positive_labels"].apply(lambda x: any([label in x for label in self.real_labels]))]
        metadata["positive_labels"] = metadata["positive_labels"].apply(lambda x: x.replace('"', ''))
        metadata = metadata.reset_index(drop=True)

        print(f"Downloading {len(metadata)} files...")

        # Download the dataset
        joblib.Parallel(n_jobs=self.n_jobs, verbose=10)(
            joblib.delayed(self.download_file)(metadata.loc[i, "YTID"], metadata.loc[i, "start_seconds"], metadata.loc[i, "end_seconds"], metadata.loc[i, "positive_labels"]) for i in tqdm(range(len(metadata)))
        )

        print("Done.")

    def download_file(
        self,
        ytid: str,
        start_seconds: float,
        end_seconds: float,
        positive_labels: str,
    ):
        """
        This method downloads a single file. It only download the audio file at 16kHz.
        If a file is associated to multiple labels, it will be stored multiple times.
        :param ytid: YouTube ID.
        :param start_seconds: start time of the audio clip.
        :param end_seconds: end time of the audio clip.
        """

        output_path = os.path.join(self.root_path, ytid+".wav")

        if os.path.exists(output_path):
            print(f"File {output_path} already exists. Skipping...")
            return
        else:
            # Download the file using yt-dlp
            os.system(f'yt-dlp -x --audio-format {self.format} --audio-quality {self.quality} --output "{os.path.join(self.root_path, ytid)}.%(ext)s" --postprocessor-args "-ss {start_seconds} -to {end_seconds}" https://www.youtube.com/watch?v={ytid}')

        return

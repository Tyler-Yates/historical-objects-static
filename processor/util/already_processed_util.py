import os.path
import pickle
from typing import Dict, Optional

from processor.util.constants import ROOT_PATH

PICKLE_FILE_PATH = os.path.join(ROOT_PATH, "already_processed.pickle")

FILE_SIZE_KEY = "size"
FILE_MTIME_KEY = "mtime"


class AlreadyProcessedUtil:
    def __init__(self):
        self.file_path_to_file_data: Optional[Dict[str, Dict]] = None

    @staticmethod
    def _load_data() -> Dict:
        if os.path.exists(PICKLE_FILE_PATH):
            with open(PICKLE_FILE_PATH, "rb") as handle:
                return pickle.load(handle)

        return {}

    def is_already_processed(self, file_path: str) -> bool:
        if self.file_path_to_file_data is None:
            self.file_path_to_file_data = self._load_data()

        file_data = self.file_path_to_file_data.get(file_path, {})

        processed_size = file_data.get(FILE_SIZE_KEY)
        file_size = os.path.getsize(file_path)
        if file_size != processed_size:
            return False

        processed_mtime = file_data.get(FILE_MTIME_KEY)
        file_mtime = os.path.getmtime(file_path)
        if file_mtime != processed_mtime:
            return False

        return True

    def record_file_processed(self, file_path: str):
        self.file_path_to_file_data[file_path] = {
            FILE_SIZE_KEY: os.path.getsize(file_path),
            FILE_MTIME_KEY: os.path.getmtime(file_path),
        }
        self._pickle_data()

    def _pickle_data(self):
        with open(PICKLE_FILE_PATH, "wb") as handle:
            pickle.dump(self.file_path_to_file_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

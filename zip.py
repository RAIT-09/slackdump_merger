import zipfile
import os

class Zip():
    @staticmethod
    def extract(file: str, dir: str):
        """
        Extract a zip file to the given directory.
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        with zipfile.ZipFile(file) as zip:
            zip.extractall(dir)

    @staticmethod
    def compress(dir: str, file: str):
        """
        Compress files in given directory.
        """
        with zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED) as zip:
            for (dirpath, dirnames, filenames) in os.walk(dir):
                for filename in filenames:
                    zip.write(dirpath + "/" + filename, dirpath.replace(dir, "") + "/" + filename)
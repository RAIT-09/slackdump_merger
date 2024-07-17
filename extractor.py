import zipfile
import os

def extract(file: str, dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with zipfile.ZipFile(file) as zip:
        zip.extractall(dir)

def compress(dir: str, file: str):
    with zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED) as zip:
        for (dirpath, dirnames, filenames) in os.walk(dir):
            for filename in filenames:
                zip.write(dirpath + "/" + filename, dirpath.replace(dir, "") + "/" + filename)

if __name__ == "__main__":
    path = "./slackdump_20240401_20240713.zip"
    extract(path)

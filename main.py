from zip import Zip
import os
import tempfile
from merger import Merger

old_dump = "./slackdump_20240401_20240713.zip"
new_dump = "./slackdump_20240401_20240725.zip"

with tempfile.TemporaryDirectory() as temp_dir:
    Zip.extract(old_dump, f"{temp_dir}/old")
    Zip.extract(new_dump, f"{temp_dir}/new")

    if not os.path.exists(f"{temp_dir}/merged"):
        os.makedirs(f"{temp_dir}/merged")
        Merger(f"{temp_dir}/old/", f"{temp_dir}/new/", f"{temp_dir}/merged/")

    Zip.compress(f"{temp_dir}/merged/", "merged.zip")
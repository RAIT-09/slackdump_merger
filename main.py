from zip import Zip
import os
from merger import Merger

old_dump = "./slackdump_20240401_20240713.zip"
new_dump = "./slackdump_20240401_20240725.zip"
Zip.extract(old_dump, "./.tmp/old")
Zip.extract(new_dump, "./.tmp/new")

if not os.path.exists("./.tmp/merged"):
    os.makedirs("./.tmp/merged")
    Merger("./.tmp/old/", "./.tmp/new/", "./.tmp/merged/")

Zip.compress("./.tmp/merged/", "merged.zip")
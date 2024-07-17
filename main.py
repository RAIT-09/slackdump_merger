import extractor
import os
from merger import Merger

old_dump = "./slackdump_20240401_20240713.zip"
new_dump = "./slackdump_20240401_20240717.zip"
extractor.extract(old_dump, "./.tmp/old")
extractor.extract(new_dump, "./.tmp/new")

if not os.path.exists("./.tmp/merged"):
    os.makedirs("./.tmp/merged")
    Merger("./.tmp/old/", "./.tmp/new/", "./.tmp/merged/")

extractor.compress("./.tmp/merged/", "merged.zip")
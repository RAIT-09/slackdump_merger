import json
from copy import deepcopy
import bisect
import os
import shutil

class Merger():
    def __init__(self, old_dir: str, new_dir: str, merged_dir: str) -> None:
        self.old_dir = old_dir
        self.new_dir = new_dir
        self.merged_dir = merged_dir

        self.file_types = ["channels", "dms", "groups", "mpims", "users"]
        self.data = {}
        self.old_data = {}
        self.new_data = {}

        for file_type in self.file_types:
            old_file = self._parse_file(f"{self.old_dir}/{file_type}.json")
            new_file = self._parse_file(f"{self.new_dir}/{file_type}.json")
            self.old_data[file_type] = old_file
            self.new_data[file_type] = new_file
            self.data[file_type] = self._merge_files(old_file, new_file)
            self._save_file(f"{file_type}.json", self.data[file_type])

        self._merge_chats()

    def _key_func(self, elem) -> str:
        return elem["id"]

    def _merge_files(self, old_elements: list, new_elements: list) -> list:
        """
        Merge two files.
        If IDs in old file doesn't exist on new file, it is a deleted channel, so insert it into newer file.
        """
        merged_elements = deepcopy(new_elements)
        new_elements_ids = {el["id"] for el in new_elements}

        for old_el in old_elements:
            if old_el["id"] not in new_elements_ids:
                insert_idx = bisect.bisect_left(
                    [self._key_func(ch) for ch in merged_elements],
                    self._key_func(old_el)
                )
                merged_elements.insert(insert_idx, old_el)

        return merged_elements

    def _merge_chats(self) -> None:
        """
        Copy chat files into appropriate directories.
        """
        new_dir_list = [f for f in os.listdir(self.new_dir) if os.path.isdir(os.path.join(self.new_dir, f))]
        old_dir_list = [f for f in os.listdir(self.old_dir) if os.path.isdir(os.path.join(self.old_dir, f))]
        chats = {}

        def add_chat(entries, dir_list, source_type, key):
            for entry in entries:
                if entry[key] in dir_list:
                    if entry["id"] not in chats:
                        chats[entry["id"]] = {}
                    chats[entry["id"]] |= {f"{source_type}_name":entry[key]}

        add_chat(self.new_data["channels"], new_dir_list, "new", "name")
        add_chat(self.new_data["dms"], new_dir_list, "new", "id")
        add_chat(self.new_data["mpims"], new_dir_list, "new", "name")
        add_chat(self.old_data["channels"], old_dir_list, "old", "name")
        add_chat(self.old_data["dms"], old_dir_list, "old", "id")
        add_chat(self.old_data["mpims"], old_dir_list, "old", "name")

        for chat_id, dirs in chats.items():
            old_name = dirs.get("old_name")
            new_name = dirs.get("new_name")
            if not old_name:
                # New channel
                shutil.copytree(f"{self.new_dir}/{new_name}", f"{self.merged_dir}/{new_name}")
            elif not new_name:
                # Removed channel
                shutil.copytree(f"{self.old_dir}/{old_name}", f"{self.merged_dir}/{old_name}")
            else:
                # Merged channel
                shutil.copytree(f"{self.old_dir}/{old_name}", f"{self.merged_dir}/{new_name}")
                shutil.copytree(f"{self.new_dir}/{new_name}", f"{self.merged_dir}/{new_name}", dirs_exist_ok = True)

    def _parse_file(self, path: str) -> list:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_file(self, file_name: str, elements: list):
        with open(self.merged_dir + "/" + file_name, "w", encoding="utf-8") as file:
            json.dump(elements, file, indent=4)

if __name__ == "__main__":
    if not os.path.exists("./.tmp/merged"):
        os.makedirs("./.tmp/merged")
    Merger("./.tmp/old/", "./.tmp/new/", "./.tmp/merged/")
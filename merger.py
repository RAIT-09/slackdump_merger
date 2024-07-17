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

        self.old_channels = self._parse_file(old_dir + "/channels.json")
        self.new_channels = self._parse_file(new_dir + "/channels.json")
        self.merged_channels = self._merge_files(self.old_channels, self.new_channels)
        self._save_file("channels.json", self.merged_channels)

        self.old_dms = self._parse_file(old_dir + "/dms.json")
        self.new_dms = self._parse_file(new_dir + "/dms.json")
        self.merged_dms = self._merge_files(self.old_dms, self.new_dms)
        self._save_file("dms.json", self.merged_dms)

        self.old_groups = self._parse_file(old_dir + "/groups.json")
        self.new_groups = self._parse_file(new_dir + "/groups.json")
        self.merged_groups = self._merge_files(self.old_groups, self.new_groups)
        self._save_file("groups.json", self.merged_groups)

        self.old_mpims = self._parse_file(old_dir + "/mpims.json")
        self.new_mpims = self._parse_file(new_dir + "/mpims.json")
        self.merged_mpims = self._merge_files(self.old_mpims, self.new_mpims)
        self._save_file("mpims.json", self.merged_mpims)

        self.old_users = self._parse_file(old_dir + "/users.json")
        self.new_users = self._parse_file(new_dir + "/users.json")
        self.merged_users = self._merge_files(self.old_users, self.new_users)
        self._save_file("users.json", self.merged_users)

        self.merge_chats()

    def _key_func(self, elem):
        return elem["id"]

    def _parse_file(self, path: str) -> list:
        with open(path, "r", encoding="utf-8") as file:
            elements = json.load(file)
            return elements

    def _merge_files(self, old_elements: list, new_elements: list) -> list:
        merged_elements = deepcopy(new_elements)
        for old_el in old_elements:
            exists = False
            for new_el in new_elements:
                if old_el["id"] == new_el["id"]: exists = True
            if not exists:
                insert_idx = bisect.bisect_left([self._key_func(ch) for ch in merged_elements], self.key_func(old_el))
                merged_elements.insert(insert_idx, old_el)
        return merged_elements

    def merge_chats(self):
        new_dir_list = [f for f in os.listdir(self.new_dir) if os.path.isdir(os.path.join(self.new_dir, f))]
        old_dir_list = [f for f in os.listdir(self.old_dir) if os.path.isdir(os.path.join(self.old_dir, f))]
        chats = {}
        for ch in self.new_channels:
            if ch["name"] in new_dir_list:
                chats[ch["id"]] = {"new_name":ch["name"]}
        for dm in self.new_dms:
            if dm["id"] in new_dir_list:
                chats[dm["id"]] = {"new_name":dm["id"]}
        for mpim in self.new_mpims:
            if mpim["name"] in new_dir_list:
                chats[mpim["id"]] = {"new_name":mpim["name"]}
        for ch in self.old_channels:
            if ch["name"] in old_dir_list:
                chats[ch["id"]] |= {"old_name":ch["name"]}
        for dm in self.old_dms:
            if dm["id"] in old_dir_list:
                chats[dm["id"]] |= {"old_name":dm["id"]}
        for mpim in self.old_mpims:
            if mpim["name"] in old_dir_list:
                chats[mpim["id"]] |= {"old_name":mpim["name"]}

        for id, dir in chats.items():
            if not "old_name" in dir:
                # new channel
                shutil.copytree(self.new_dir + "/" + dir["new_name"], self.merged_dir + "/" + dir["new_name"])
            elif not "new_name" in dir:
                # removed channel
                shutil.copytree(self.old_dir + "/" + dir["old_name"], self.merged_dir + "/" + dir["old_name"])
            else:
                shutil.copytree(self.old_dir + "/" + dir["old_name"], self.merged_dir + "/" + dir["new_name"])
                shutil.copytree(self.new_dir + "/" + dir["new_name"], self.merged_dir + "/" + dir["new_name"], dirs_exist_ok = True)

    def _save_file(self, file_name: str, elements: list):
        with open(self.merged_dir + "/" + file_name, "w", encoding="utf-8") as file:
            json.dump(elements, file, indent=4)

if __name__ == "__main__":
    if not os.path.exists("./.tmp/merged"):
        os.makedirs("./.tmp/merged")
    Merger("./.tmp/old/", "./.tmp/new/", "./.tmp/merged/")
class ItemInfoCogg:
    import pathlib
    import json
    def __init__(self):
        cwd_path = self.pathlib.PurePath(self.pathlib.Path(__file__))
        self.main_path = str(cwd_path.parents[2])
        with self.pathlib.Path(self.main_path, "resources", "parseditems.json").open("r") as f:
            self.ingameitems = self.json.load(f)

    def check(self, author, content, chat_queue, logger):
        if content.startswith("iteminfo"):
            item_name = content[9:]
            if item_name in ["", " "]:
                chat_queue.put("that item does not exist!")
                return True
            for item in self.ingameitems:
                if type(item) is dict:
                    if item["name"].lower() == item_name.lower():
                        chat_queue.put(item["description"])
                        return True
            possible_meanings = ""
            poss_meanings = []
            for item in self.ingameitems:
                if type(item) is dict:
                    if item_name.lower() in item["name"].lower():
                        possible_meanings += item["name"] + ", "
                        poss_meanings.append(item)
            if possible_meanings != "":
                if len(poss_meanings) < 7:
                    chat_queue.put(f"That's not a item! did you mean one of these? {possible_meanings}")
                    return True
                else:
                    chat_queue.put(f"Please be more spacific - there are {len(poss_meanings)} items that include {item_name}")
                    return True
            else:
                chat_queue.put("that item does not exist!")
                return True
            return False

module_coggs = [ItemInfoCogg]
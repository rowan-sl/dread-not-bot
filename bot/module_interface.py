import pathlib
import importlib
import yaml
import re
import queue

class ModuleController:
    def __init__(self, logger, chat_queue: queue.Queue) -> None:
        self.logger = logger
        self.chat_queue = chat_queue
        # get index/modules dir
        index_path = str(pathlib.PurePath(pathlib.Path(__file__).parents[1], "bot", "modules", "index.yaml")) #yeet
        # retreve index of modules
        with open(index_path,'r') as f:
            modules_index = list(yaml.safe_load_all(f))
        self.modules = modules_index[0]['modules']
        #? better way of importing modules
        #? this is becaues it does not ever use exec() or eval(), but stores the imported module in an array :0, this also means you can run it without exec or eval
        self.imported = []
        for module in self.modules:
            self.logger.debug(f"Importing {module}")
            try:
                self.imported.append(importlib.import_module(f"modules.{module}_cogg"))
            except ImportError as e:
                self.logger.warning(f"Failed to import {module}, because {repr(e)}")
        self.logger.detail(f"Sucsesfully imported {self.imported}")
        
    def interpet(self, author, content) -> None:
        for loaded_module in self.imported:
            response = loaded_module.check(author, content, loaded_module, self.chat_queue, self.logger)# oooh look it dosent use eval()
            if response is not False or None:
                return True
        return False
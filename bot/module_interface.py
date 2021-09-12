import pathlib
import importlib
import yaml
import re
import queue
import dill, gzip
import sys

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
        self.bin_modules = modules_index[0]['bin_modules']
        #? better way of importing modules
        #? this is becaues it does not ever use exec() or eval(), but stores the imported module in an array :0, this also means you can run it without exec or eval
        self.imported = []
        if self.modules is not None:
            for module in self.modules:
                self.logger.detail(f"Importing {module}")
                try:
                    self.imported.append(importlib.import_module(f"modules.{module}_cogg"))
                except ImportError as e:
                    self.logger.warning(f"Failed to import {module}, because {repr(e)}")
            self.logger.detail(f"Sucsesfully imported {self.imported}")
        coggs = []
        self.instances = []
        for module in self.imported:
            for Cogg in module.module_coggs:
                coggs.append(Cogg)
        # get modules compressed from coggs
        cwd_path = pathlib.PurePath(pathlib.Path(__file__))
        main_path = str(cwd_path.parents[1])
        if self.bin_modules is not None:
            for module in self.bin_modules:
                path = pathlib.Path(main_path, "bot", "modules", "bin", f"{module}.cogg.bin")
                with path.open("rb") as f:
                    squashed_bitez = f.read()
                    bitez = gzip.decompress(squashed_bitez)
                    cogg = dill.loads(bitez)
                    coggs.append(cogg)
        for Cogg in coggs:
            self.instances.append(Cogg())
        self.logger.detail(str(self.instances))
        self.logger.detail(str(coggs))

    
    def interpet(self, author, content) -> bool:
        self.logger.detail("running check")
        for CoggInstance in self.instances:
            self.logger.detail(f'running check for {CoggInstance}')
            response = CoggInstance.check(author, content, self.chat_queue, self.logger)
            if not ((response is None) or (response is False)):
                self.logger.detail("module gave answer")
                return True
        self.logger.detail("no command")
        return False
import pathlib
import os, sys
import dill
import gzip
import yaml
import importlib

cwd_path = pathlib.PurePath(pathlib.Path(__file__))
main_path = str(cwd_path.parents[2])
index_path = str(pathlib.PurePath(main_path, "bot", "modules", "index.yaml")) #yeet
sys.path.append(main_path)

with open(index_path,'r') as f:
    modules_index = list(yaml.safe_load_all(f))
    modules = modules_index[0]['modules_gen']

imported = []
if modules is not None:
    for module in modules:
        try:
            imported.append(importlib.import_module(f"bot.modules.{module}_cogg"))
        except ImportError as e:
            print(f"failed to import {module} because of {e}")
    print(f"imported {imported}")

for module in imported:
    for Cogg in module.module_coggs:
        bitez = dill.dumps(Cogg, byref=True)
        squashed_bitez = gzip.compress(bitez, 9)
        # print(f'writing to {pathlib.PurePath(main_path, "bot", "modules", "bin", f"{Cogg.__name__.lower()[:-4]}.cogg.bin")}')
        if not Cogg.__name__.lower().endswith("cogg"):
            raise ValueError("class name must end with cogg")
            break
        with pathlib.Path(main_path, "bot", "modules", "bin", f"{Cogg.__name__.lower()[:-4]}.cogg.bin").open("wb") as f:
            f.write(squashed_bitez)
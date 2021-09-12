import pathlib
import os, sys
import dill
import gzip

cwd_path = pathlib.PurePath(pathlib.Path(__file__))
main_path = str(cwd_path.parents[2])
sys.path.append(main_path)

#import thing to compress here
from bot.modules.builtin_cogg import BuiltinCogg

bitez = dill.dumps(BuiltinCogg, byref=True)
squashed_bitez = gzip.compress(bitez, 9)
with pathlib.Path(main_path, "bot", "modules", "bin", "builtin.cogg.bin").open("wb") as f:
    f.write(squashed_bitez)

with pathlib.Path(main_path, "bot", "modules", "bin", "builtin.cogg.bin").open("rb") as f:
    squashed_bitez = f.read()
    bitez = gzip.decompress(squashed_bitez)
    cogg = dill.loads(bitez)
instance = cogg()
instance.check()
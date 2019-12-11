import os
import re

DATA_DIR = "de-en/"

for file in filter(lambda x: x.endswith(".xml"), os.listdir(DATA_DIR)):
    with open(os.path.join(DATA_DIR, file), "r") as f:
        lines = filter(lambda x: x.startswith("<seg id"), f.readlines())
        lines = list(map(lambda x: re.findall('^<seg id="\w*">\s*(.*)\s*</seg>\s*$', x)[0], lines))
    with open(os.path.join(DATA_DIR, re.sub(".xml", ".parsed", file)), "w") as f:
        f.write("\n".join(lines))

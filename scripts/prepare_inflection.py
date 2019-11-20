import argparse
import os
import re
import codecs

parser = argparse.ArgumentParser(description="Inflection Parser")
parser.add_argument("--data", type=str,
                    help="folder with *-train-* files")
parser.add_argument("--save_to", type=str,
                    help="folder for preprocessed files")

def preprocess(lines):
    src = []
    tgt = []
    for line in lines:
        sep = "\t"
        line = line.strip().split(sep)
        src.append(" ".join(line[2].split(';')) + " " + " ".join(line[0]))
        tgt.append(" ".join(line[1]))
    return src, tgt


def main(args):
    with open(args.save_to + "high.train.src", "w", encoding="utf-8") as f_src:
        with open(args.save_to + "high.train.tgt", "w", encoding="utf-8") as f_tgt:
            for lang in sorted(list({re.sub('\-train.*$','',d) for d in os.listdir(args.data) if '-train-' in d})):
                for quantity in ['high']:
                    file_train = args.data + lang +  "-train-" + quantity
                    if not os.path.isfile(file_train):
                        continue
                    lines = [line.strip() for line in codecs.open(file_train, "r", encoding="utf-8")]
                    src, tgt = preprocess(lines)
                    for line in src:
                        f_src.write(line)
                        f_src.write("\n")
                    for line in tgt:
                        f_tgt.write(line)
                        f_tgt.write("\n")
    with open(args.save_to + "high.dev.src", "w", encoding="utf-8") as f_src:
        with open(args.save_to + "high.dev.tgt", "w", encoding="utf-8") as f_tgt:
            for lang in sorted(list({re.sub('\-train.*$','',d) for d in os.listdir(args.data) if '-train-' in d})):
                file_name = args.data + lang +  "-train-" + quantity
                if not os.path.isfile(file_name):
                    continue
                lines = [line.strip() for line in codecs.open(args.data + lang + "-dev", "r", encoding="utf-8")]
                src, tgt = preprocess(lines)
                for line in src:
                    f_src.write(line)
                    f_src.write("\n")
                for line in tgt:
                    f_tgt.write(line)
                    f_tgt.write("\n")

if __name__=="__main__":
    args = parser.parse_args()
    main(args)
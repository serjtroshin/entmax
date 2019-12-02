import argparse
import os
import re
import codecs
import pickle

parser = argparse.ArgumentParser(description="Inflection Parser")
parser.add_argument("--data", type=str,
                    help="folder with *-train-* files")
parser.add_argument("--save_to", type=str,
                    help="folder for preprocessed files")

SPACE = "<space>"
def preprocess(lines):
    src = []
    tgt = []
    for line in lines:
        sep = "\t"
        line = line.strip().split(sep)
        new_src = "$".join(line[2].split(';')).replace(" ", SPACE) + "$#$" + "$".join(line[0]).replace(" ", SPACE)
        src.append(new_src.replace("$", " "))
        new_tgt = "$".join(line[1]).replace(" ", SPACE)
        tgt.append(new_tgt.replace("$", " "))
    return src, tgt


def main(args):
    with open(args.save_to + "high.train.src", "w", encoding="utf-8") as f_src:
        with open(args.save_to + "high.train.tgt", "w", encoding="utf-8") as f_tgt:
            for lang in sorted(list({re.sub('\-train.*$','',d) for d in os.listdir(args.data) if '-train-' in d})):
                for quantity in ['high']:
                    file_train = args.data + lang +  "-train-" + quantity
                    if not os.path.isfile(file_train):
                        continue
                    print("file_train:", file_train)
                    lines = [line.strip() for line in codecs.open(file_train, "r", encoding="utf-8")]
                    src, tgt = preprocess(lines)
                    for line in src:
                        f_src.write(line)
                        f_src.write("\n")
                    for line in tgt:
                        f_tgt.write(line)
                        f_tgt.write("\n")
    languages2lines = {}
    line_cnt = 0
    with open(args.save_to + "high.dev.src", "w", encoding="utf-8") as f_src:
        with open(args.save_to + "high.dev.tgt", "w", encoding="utf-8") as f_tgt:
            for lang in sorted(list({re.sub('\-train.*$','',d) for d in os.listdir(args.data) if '-train-' in d})):
                start = line_cnt
                file_name = args.data + lang +  "-dev"
                if not os.path.isfile(file_name):
                    continue
                print("file_dev:", file_name)
                lines = [line.strip() for line in codecs.open(args.data + lang + "-dev", "r", encoding="utf-8")]
                end = start + len(lines)
                src, tgt = preprocess(lines)
                for line in src:
                    f_src.write(line)
                    f_src.write("\n")
                for line in tgt:
                    f_tgt.write(line)
                    f_tgt.write("\n")
                line_cnt += len(lines)
                languages2lines[lang] = (start, end)
    with open(f"{args.save_to}/lang2lines.pkz", "wb") as fff:
        pickle.dump(languages2lines, fff)

if __name__=="__main__":
    args = parser.parse_args()
    main(args)

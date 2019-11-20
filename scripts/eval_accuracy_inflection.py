import argparse
import os
import re
import codecs
import pickle

parser = argparse.ArgumentParser(description="Accuracy Parser")
parser.add_argument("--directory", type=str, default="data",
                    help="folder with files")
parser.add_argument("--data_true", type=str, default="high.dev.tgt",
                    help="file with gold data")
parser.add_argument("--data_pred", type=str, default="pred.txt",
                    help="file with predicted data")
parser.add_argument("--lang2lines", type=str, default="lang2lines.pkz",
                    help="matching between languages and lines in files")
    
def accuracy(pred, gold):
    ans = []
    for p, g in zip(pred, gold):
        ans.append(p == g)
    return sum(ans) * 1.0 / len(ans), ans

def main(args):
    with open(os.path.join(args.directory, args.data_pred), "r") as f:
        pred = f.readlines()
    with open(os.path.join(args.directory, args.data_true), "r") as f:
        gold = f.readlines()
    with open(os.path.join(args.directory, args.lang2lines), "rb") as f:
        lang2lines = pickle.load(f)
    accuracies = []
    anses = []
    print("Languages:", lang2lines)
    for lang, (start, end) in lang2lines.items():
        predl = pred[start:end]
        goldl = gold[start:end]
        acc_lang, ans = accuracy(predl, goldl)
        accuracies.append(acc_lang)
        anses.extend(ans)
    print(f"Accuracy for {len(lang2lines.keys())} langs = {sum(accuracies)/len(accuracies):.2f}")
    print(f"Accuracy for all words {sum(anses) * 1.0/ len(anses):.2f}")


if __name__=="__main__":
    args = parser.parse_args()
    main(args)



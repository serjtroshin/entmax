mkdir data
cd OpenNMT-py
dir="../"
src=$1
tgt=$2
pair="$1-$2"
python preprocess.py \
-train_src $dir/de-en/train.$pair.$src.tok.truecased.bpe \
-train_tgt $dir/de-en/train.$pair.$tgt.tok.truecased.bpe \
-valid_src $dir/de-en/dev.$pair.$src.tok.truecased.bpe \
-valid_tgt $dir/de-en/dev.$pair.$tgt.tok.truecased.bpe \
-overwrite -save_data $dir/data/iwlst.$pair
